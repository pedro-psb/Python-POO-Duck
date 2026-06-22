def inteiro_positivo(valor: int, nao_nulo: bool) -> int:
    """Valida se o valor é um número inteiro positivo (ou não-negativo) e o retorna."""
    if not isinstance(valor, int):
        raise ValueError("O valor deve ser um número inteiro.")
    if nao_nulo and valor <= 0:
        raise ValueError("O valor deve ser maior do que zero.")
    if not nao_nulo and valor < 0:
        raise ValueError("O valor deve ser maior ou igual a zero.")
    return valor
