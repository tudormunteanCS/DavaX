import click
import requests
import base64
import asyncio


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


async def greet(name):
    await asyncio.sleep(1)
    print(f"Hello {name}")


async def main():
    await asyncio.gather(
        greet("Bob"),
        greet("Alice"),
        greet("Charlie")
    )


async def async_hello():
    await asyncio.sleep(2)
    print("Hello, world!")


if __name__ == '__main__':
    # r = requests.get(
    #     "https://httpbin.org/digest-auth/auth/user/passwd",
    #     auth=requests.auth.HTTPDigestAuth('user', 'passwd')
    # )
    # print(r.status_code)

    asyncio.run(async_hello())

    # asyncio.run(main())
