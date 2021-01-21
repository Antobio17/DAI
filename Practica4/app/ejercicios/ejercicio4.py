def Fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        fibonacci_term_n = 0
        fibonacci_term_n_1 = 1
        fibonacci_term_n_2 = 0
        for i in range(n-1):
            fibonacci_term_n = fibonacci_term_n_2 + fibonacci_term_n_1
            fibonacci_term_n_2 = fibonacci_term_n_1
            fibonacci_term_n_1 = fibonacci_term_n
        return fibonacci_term_n