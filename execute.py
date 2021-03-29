for _ in range(1000):
    with open("main.py", "r") as f:
        exec(f.read())
