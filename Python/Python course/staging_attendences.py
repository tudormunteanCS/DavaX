import os
import pandas as pd
import oracledb


def get_oracle_connection() -> oracledb.Connection:
    """
    creates an oracle Connection
    :return: oracledb.Connection
    """
    return oracledb.connect(
        user="hr",
        password="oracle",
        dsn="localhost:1521/xepdb1"
    )


def parse_duration(duration: str) -> int:
    """
    parses a string duration and returns the numbers of seconds
    example: input: 1h 28m 6s output: 1 * 3600 + 28 * 60 + 6
    :param duration: String
    :return: number of seconds as an integer
    """
    parts = duration.strip().split()
    seconds = 0
    for part in parts:
        if 'h' in part:
            seconds += int(part.replace('h', '')) * 3600
        elif 'm' in part:
            seconds += int(part.replace('m', '')) * 60
        else:
            seconds += int(part.replace('s', ''))

    return seconds


def insert_into_db(df: pd.DataFrame,meeting_id: int) -> None:
    """
    creates a connection to the oracle db and inserts each row into staging table
    :param df: DataFrame
    :return:
    """
    conn = get_oracle_connection()
    cursor = conn.cursor()
    insert_statement = """
                       INSERT INTO StagingAttendance(meeting_id,
                                                     name,
                                                     first_join,
                                                     last_join,
                                                     in_meeting_duration,
                                                     email,
                                                     role_employee)
                       Values (:1,
                               :2,
                               TO_DATE(:3, 'MM/DD/YY HH:MI:SS PM'),
                               TO_DATE(:4, 'MM/DD/YY HH:MI:SS PM'),
                               :5,
                               :6,
                               :7) \
                       """

    for _, row in df.iterrows():
        cursor.execute(insert_statement, (
            meeting_id,
            row['Name'],
            row['First Join'],
            row['Last Leave'],
            parse_duration(row['In-Meeting Duration']),
            row['Email'],
            row['Role']
        ))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    directory = 'attendences'
    meeting_id = 6
    for attendence in os.listdir(directory):
        path = os.path.join(directory, attendence)
        df = pd.read_excel(path, skiprows=9)  # collect only participants
        first_empty_index = df[
            df.isnull().all(axis=1)].index.min()  # find first empty line marking the end of employees
        df = df.iloc[:first_empty_index]  # trim the data frame
        insert_into_db(df,meeting_id)
        meeting_id += 1
