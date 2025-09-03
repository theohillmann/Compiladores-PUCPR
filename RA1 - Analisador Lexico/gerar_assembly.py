def is_integer(token):
    """
    Verifica se o token é um número inteiro.

    Args:
        token (str): Token a ser verificado.

    Returns:
        bool: True se for inteiro, False caso contrário.
    """
    try:
        int(token)
        return True
    except:
        return False


def is_variable(token):
    """
    Verifica se o token é uma variável válida (alfabética e diferente de 'RES').

    Args:
        token (str): Token a ser verificado.

    Returns:
        bool: True se for variável, False caso contrário.
    """
    return token.isalpha() and token != "RES"


def flatten(tokens):
    """
    Remove parênteses da lista de tokens.

    Args:
        tokens (list): Lista de tokens.

    Returns:
        list: Lista de tokens sem parênteses.
    """
    return [t for t in tokens if t not in ("(", ")")]


def get_variable_label(name, st):
    """
    Obtém ou cria o rótulo de uma variável.

    Args:
        name (str): Nome da variável.
        st (dict): Estado contendo os rótulos.

    Returns:
        str: Rótulo da variável.
    """
    k = name.lower()
    if k not in st["var_labels"]:
        st["var_labels"][k] = f"var_{k}"
    return st["var_labels"][k]


def emit_load(desc, reg):
    """
    Gera instruções para carregar um valor imediato ou de memória em um registrador.

    Args:
        desc (tuple): Descrição do valor ('imm' ou 'var', valor).
        reg (str): Registrador de destino.

    Returns:
        list: Lista de instruções assembly.
    """
    kind, value = desc
    if kind == "imm":
        return [f"        ldi {reg},{value & 0xFF}"]
    else:
        return [f"        lds {reg},{value}"]


def emit_operation(a, b, op, st):
    """
    Gera instruções para realizar uma operação aritmética entre dois operandos.

    Args:
        a (tuple): Operando esquerdo.
        b (tuple): Operando direito.
        op (str): Operação ('+', '-', '*', '/', '%', '^').
        st (dict): Estado para controle de temporários.

    Returns:
        tuple: (Lista de instruções, descrição do resultado).
    """
    lines = []
    if op == "/":
        st["tmp_counter"] += 1
        t = f"tmp_{st['tmp_counter']}"
        dlabel, rlabel = f"{t}_div", f"{t}_rem"
        st["tmp_labels"].append(t)
        st["div_info"][t] = (dlabel, rlabel)
        lines += emit_load(a, "r16") + emit_load(b, "r17")
        lines += [
            f"        sts {dlabel},r17",
            "        rcall div_loop",
            f"        sts {rlabel},r17",
            f"        sts {t},r16",
        ]
        return lines, ("tmpdiv", t)
    lines += emit_load(a, "r16") + emit_load(b, "r17")
    if op == "+":
        lines.append("        add r16,r17")
    elif op == "-":
        lines.append("        sub r16,r17")
    elif op == "*":
        lines.append("        rcall mul_loop")
    elif op == "%":
        lines += ["        rcall div_loop", "        mov r16,r17"]
    elif op == "^":
        lines.append("        rcall pow_loop")
    st["tmp_counter"] += 1
    t = f"tmp_{st['tmp_counter']}"
    st["tmp_labels"].append(t)
    lines.append(f"        sts {t},r16")
    return lines, ("tmp", t)


def gerarAssembly(expressions):
    """
    Gera o código assembly a partir de uma lista de expressões.

    Args:
        expressions (list): Lista de expressões tokenizadas.

    Returns:
        str: Código assembly gerado.
    """
    ops = {"+", "-", "*", "/", "%", "^"}
    st = {
        "var_labels": {},
        "tmp_labels": [],
        "res_labels": [],
        "div_info": {},
        "tmp_counter": 0,
        "res_counter": 0,
    }

    out = [
        "        .section .text",
        "        .global main",
        "",
        "main:",
        "        clr r1",
        "        ldi r16,0",
        "        sts 0x00C5,r16",
        "        ldi r16,0x67",
        "        sts 0x00C4,r16",
        "        ldi r16,0x08",
        "        sts 0x00C1,r16",
        "        ldi r16,0x06",
        "        sts 0x00C2,r16",
        "",
    ]

    for expr in expressions:
        tokens = flatten(expr)

        if (
            len(tokens) == 2
            and is_variable(tokens[1])
            and not any(t in ops for t in tokens)
        ):
            val, name = tokens
            desc = (
                ("imm", int(val))
                if is_integer(val)
                else ("var", get_variable_label(val, st))
            )
            label = get_variable_label(name, st)
            out += emit_load(desc, "r16") + [f"        sts {label},r16", ""]
            continue

        stack = []
        code = []
        for t in tokens:
            if is_integer(t):
                stack.append(("imm", int(t)))
            elif is_variable(t):
                stack.append(("var", get_variable_label(t, st)))
            elif t == "RES":
                k = 1
                if stack and stack[-1][0] == "imm":
                    k = stack.pop()[1]
                stack.append(
                    (
                        "res",
                        (
                            st["res_labels"][-k]
                            if 1 <= k <= len(st["res_labels"])
                            else "zero"
                        ),
                    )
                )
            elif t in ops:
                b = stack.pop()
                a = stack.pop()
                el, desc = emit_operation(a, b, t, st)
                code += el
                stack.append(desc)

        if not stack:
            out.append("")
            continue

        fk, fv = stack.pop()
        if fk == "imm":
            code += emit_load(("imm", fv), "r16")
        elif fk in ("var", "res"):
            code += emit_load((fk, fv), "r16")
        elif fk == "tmp":
            code += emit_load(("tmp", fv), "r16")

        if any(t in ops for t in tokens):
            st["res_counter"] += 1
            rlbl = f"res_{st['res_counter']}"
            st["res_labels"].append(rlbl)
            if fk == "tmpdiv":
                code += [
                    f"        lds r16,{fv}",
                    f"        sts {rlbl},r16",
                    f"        lds r16,{fv}",
                    f"        lds r17,{st['div_info'][fv][1]}",
                    f"        lds r18,{st['div_info'][fv][0]}",
                    "        rcall print_div_dec",
                ]
            else:
                code += [f"        sts {rlbl},r16", "        rcall print_num_signed"]
            code += ["        rcall newline"]

        out += code + [""]

    out += [
        "end:",
        "        rjmp end",
        "",
        "send:",
        "        push r17",
        "wait:",
        "        lds r17,0x00C0",
        "        sbrs r17,5",
        "        rjmp wait",
        "        sts 0x00C6,r16",
        "        pop r17",
        "        ret",
        "",
        "newline:",
        "        push r16",
        "        ldi r16,13",
        "        rcall send",
        "        ldi r16,10",
        "        rcall send",
        "        pop r16",
        "        ret",
        "",
        "print_num:",
        "        push r17",
        "        push r18",
        "        push r19",
        "        push r20",
        "        mov r18,r16",
        "        clr r19",
        "        clr r20",
        "hunds:",
        "        cpi r18,100",
        "        brlo tens",
        "        subi r18,100",
        "        inc r19",
        "        rjmp hunds",
        "tens:",
        "        cpi r18,10",
        "        brlo ones",
        "        subi r18,10",
        "        inc r20",
        "        rjmp tens",
        "ones:",
        "        tst r19",
        "        breq maybe_tens",
        "        mov r16,r19",
        "        ldi r17,48",
        "        add r16,r17",
        "        rcall send",
        "maybe_tens:",
        "        tst r19",
        "        brne print_tens",
        "        tst r20",
        "        breq print_units",
        "print_tens:",
        "        mov r16,r20",
        "        ldi r17,48",
        "        add r16,r17",
        "        rcall send",
        "print_units:",
        "        mov r16,r18",
        "        ldi r17,48",
        "        add r16,r17",
        "        rcall send",
        "        pop r20",
        "        pop r19",
        "        pop r18",
        "        pop r17",
        "        ret",
        "",
        "print_num_signed:",
        "        sbrs r16,7",
        "        rjmp ppos",
        "        push r16",
        "        ldi r16,45",
        "        rcall send",
        "        pop r16",
        "        com r16",
        "        inc r16",
        "ppos:",
        "        rcall print_num",
        "        ret",
        "",
        "div_loop:",
        "        push r18",
        "        push r19",
        "        mov r18,r16",
        "        mov r19,r17",
        "        clr r16",
        "        tst r19",
        "        brne dgo",
        "        mov r17,r18",
        "        pop r19",
        "        pop r18",
        "        ret",
        "dgo:",
        "        cp r18,r19",
        "        brlo dstore",
        "        sub r18,r19",
        "        inc r16",
        "        rjmp dgo",
        "dstore:",
        "        mov r17,r18",
        "        pop r19",
        "        pop r18",
        "        ret",
        "",
        "mul_loop:",
        "        push r18",
        "        push r19",
        "        mov r18,r16",
        "        mov r19,r17",
        "        clr r16",
        "mgo:",
        "        tst r19",
        "        breq mend",
        "        add r16,r18",
        "        dec r19",
        "        rjmp mgo",
        "mend:",
        "        pop r19",
        "        pop r18",
        "        ret",
        "",
        "pow_loop:",
        "        push r18",
        "        push r19",
        "        sts pow_base,r16",
        "        ldi r16,1",
        "pow_go:",
        "        tst r17",
        "        breq pow_end",
        "        lds r19,pow_base",
        "        push r17",
        "        mov r17,r19",
        "        rcall mul_loop",
        "        pop r17",
        "        dec r17",
        "        rjmp pow_go",
        "pow_end:",
        "        pop r19",
        "        pop r18",
        "        ret",
        "",
        "print_div_dec:",
        "        push r17",
        "        push r18",
        "        push r19",
        "        push r20",
        "        push r21",
        "        push r22",
        "        rcall print_num",
        "        ldi r16,46",
        "        rcall send",
        "        mov r19,r17",
        "        clr r20",
        "        clr r21",
        "        ldi r22,100",
        "sum100:",
        "        tst r22",
        "        breq div16",
        "        add r20,r19",
        "        adc r21,r1",
        "        dec r22",
        "        rjmp sum100",
        "div16:",
        "        clr r17",
        "divrun:",
        "        tst r21",
        "        brne dsub",
        "        cp r20,r18",
        "        brlo done2",
        "dsub:",
        "        sub r20,r18",
        "        sbc r21,r1",
        "        inc r17",
        "        rjmp divrun",
        "done2:",
        "        mov r16,r17",
        "        cpi r16,10",
        "        brsh two",
        "        ldi r16,48",
        "        rcall send",
        "        mov r16,r17",
        "two:",
        "        rcall print_num",
        "        pop r22",
        "        pop r21",
        "        pop r20",
        "        pop r19",
        "        pop r18",
        "        pop r17",
        "        ret",
        "",
        "        .section .bss",
        "zero:",
        "        .skip 1",
        "pow_base:",
        "        .skip 1",
    ]

    for label in st["var_labels"].values():
        out += [f"{label}:", "        .skip 1"]
    for t in st["tmp_labels"]:
        out += [f"{t}:", "        .skip 1"]
        if t in st["div_info"]:
            d, r = st["div_info"][t]
            out += [f"{d}:", "        .skip 1", f"{r}:", "        .skip 1"]
    for k in range(1, st["res_counter"] + 1):
        out += [f"res_{k}:", "        .skip 1"]

    asm = "\n".join(out)
    if not asm.endswith("\n"):
        asm += "\n"
    return asm
