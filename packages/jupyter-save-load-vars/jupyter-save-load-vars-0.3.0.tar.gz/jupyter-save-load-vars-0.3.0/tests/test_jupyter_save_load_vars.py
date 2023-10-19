# jupyter-save-load-vars tests for pytest.
# to test,` pip install pytest`, then run `pytest` from root of project (..)
import logging

from jupyter_save_load_vars import savevars,loadvars,printvars,_DEFAULT_FILENAME,_DILL_EXTENSION
import functools, sys
import time

print = functools.partial(print, flush=True, file=sys.stderr)  # flush and put print() on stderr so logging comes in sequence


def test_nonexisting_file():
    # test nonexisting file
    try:
        loadvars('idontexist')
        return False
    except Exception as e:
        return True


def test_vars_save_load(monkeypatch): # https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call

    lev=logging.DEBUG
    def set_input(mystr):
        # monkeypatch the "input" function, so that it returns "Mark".
        # This simulates the user entering "Mark" in the terminal:
        if monkeypatch:
            print(f'simulating input {mystr}')
            monkeypatch.setattr('builtins.input', lambda _: mystr)
        else:
            print(f'not installing monkeypatch for input {mystr}')

    set_input('y')
    print('testing savevars with no local variables, should overwrite if it exists already')
    savevars(logging_level=lev)

    set_input('n')
    print('testing savevars with no local variables, should NOT overwrite if it exists already')
    savevars(logging_level=lev)

    # create some vars
    print('creating some variables')
    a=1
    a1=11
    b=[2,3]
    c='string'
    o=(i for i in []) # make generator that cannot be pickled
    In=[1,2,'3'] # should not be saved (standard notebook var)
    Out=['an Out string'] # should not be saved
    _a13='underscore var' # should not be saved, used by notebook for commands

    # define a class, should not be saved
    class MyClass:
        name = ""
        l=[1,2,3]
    cl = MyClass() # create object with this class
    print('testing printvars()')
    printvars()


    print('testing default savevars() again with variables')
    savevars(logging_level=lev)
    set_input('n')
    savevars(logging_level=lev)
    set_input('y')
    savevars(logging_level=lev)

    print('testing loadvars() again with variables')

    loadvars(logging_level=lev)
    printvars(logging_level=lev)
    print('saving all variables')

    savevars('allvars',overwrite=True)
    print('saving only b,c variables')
    set_input('y')
    savevars('partvars',['b','c'])
    print('saving only vars starting with a')
    savevars('avars.dill','a*')
    del a,a1,b
    loadvars('avars', logging_level=logging.DEBUG)
    try:
        print(f'a={a} a1={a1}')
    except:
        pass

    try:
        print(f'b={b}')
        raise AssertionError('b should not exist')
    except: # it should cause exception
        pass


    print('deleting c')
    del c
    print('loading variables with prompt (default)')
    loadvars('allvars')  # load with prompt for overwriting existing a variable
    print('loading variables with no overwrite')
    loadvars('allvars', overwrite='no')
    loadvars('allvars', overwrite=False)
    print('loading variables with overwrite')
    loadvars('allvars', overwrite='yes')
    loadvars('allvars', overwrite=True)
    printvars()
    # del a,b,c,cl,o
    print('loading only b,c saved earlier')
    loadvars('partvars')
    printvars()

    print('cleaning up')
    import os
    for i in ['allvars','partvars','avars',_DEFAULT_FILENAME]:
        try:
            f=i+_DILL_EXTENSION
            os.remove(f)
            print(f'deleted {f}')
        except:
            pass


# uncomment to run this test from command line directly, just as a script
# if __name__ == '__main__':
#     test_nonexisting_file()
#     test_vars_save_load()