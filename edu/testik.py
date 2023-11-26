from decorators import do_twice

@do_twice
def echo(blya):
    print(f"SUKA1 {blya}")
    return blya + "   NAHUI"
print(echo("BLYA"))