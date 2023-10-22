def first_function():
    a = 3 
    print ('a', a)
    return a
def second_function():
    b = 4
    c = a+b
    print (a, b, c)
    return b,c
def myf():
    print ('hello')
    a = 3
    b = 4
    c = 5
    d = a+b+c
    return b,a
def myf():
    print ('hello')
    a = 3
    b = 4
    c = 5
    d = a+b+c
    return d,c,b,a
def myf():
    print ('hello')
    a = 3
    b = 4
    c = 5
    d = a+b+c
    return d,c,b,a
def my_defined_function (x, a=3):

    print (x)
    print (a)

def nbdev_sync_pipeline (test=False, load=True, save=True, result_file_name="nbdev_sync_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("nbdev_sync") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    a = first_function ()
    b, c = second_function ()
    b, a = myf ()
    d, c, b, a = myf ()
    d, c, b, a = myf ()
    my_defined_function (x, a)

    # save result
    result = Bunch (b=b,a=a,d=d,c=c)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
