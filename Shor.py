proc FindFactors N
  x = 0

  if N < 15
    Print "Nombre non valide!"
    Breakpoint
  endif

  width = QMath.getWidth(N)
  twidth = 2 * width + 3

  for x; (QMath.gcd(N, x) > 1) || (x < 2); x
    x = Math.floor(Math.random() * 10000) % N
  endfor

  Print "Random seed: " + x

  for i = 0; i < twidth; i++
    Hadamard i
  endfor

  ExpModN x, N, twidth

  for i = 0; i < width; i++
    MeasureBit twidth + i
  endfor

  InvQFT 0, twidth

  for i = 0; i < twidth / 2; i++
    Swap i, twidth - i - 1
  endfor

  for trycnt = 100; trycnt >= 0; trycnt--
    Measure
    c = measured_value

    if c == 0
      Print "Measured zero, try again."
      continue
    endif

    q = 1 << width

    Print "Measured " + c + " (" + c / q + ")"

    tmp = QMath.fracApprox(c, q, width)

    c = tmp[0];
    q = tmp[1];

    Print "fractional approximation is " + c + "/" + q

    if (q % 2 == 1) && (2 * q < (1 << width))
      Print "Odd denominator, trying to expand by 2."
      q *= 2
    endif

    if q % 2 == 1
      Print "Odd period, try again."
      continue
    endif

    Print "Possible period is " + q

    a = QMath.ipow(x, q / 2) + 1 % N
    b = QMath.ipow(x, q / 2) - 1 % N

    a = QMath.gcd(N, a)
    b = QMath.gcd(N, b)

    if a > b
      factor = a
    else
      factor = b
    endif

    if (factor < N) && (factor > 1)
      Display "<h2>Success: " + factor + " " + N / factor
      Breakpoint
    else
      Print "Unable to determine factors, try again."
      continue
    endif
  endfor
endproc

VectorSize 16
FindFactors 15
