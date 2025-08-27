# arquivo: posts/cursos/matematica/calculo/code/r/taxa_variacao_intro.R
# Aproximação de inclinações de secantes e visualização básica

secant_slopes <- function(f, x0, hs) {
  ms <- sapply(hs, function(h) (f(x0 + h) - f(x0)) / h)
  data <- data.frame(h = hs, m_sec = ms)
  rownames(data) <- NULL
  return(data)
}

plot_secants <- function(f, x0, hs, window = c(x0 - 3, x0 + 3)) {
  xs <- seq(window[1], window[2], length.out = 400)
  ys <- sapply(xs, f)

  plot(xs, ys, type = "l", lwd = 2, xlab = "x", ylab = "f(x)")
  abline(v = x0, lty = 3)

  h_big  <- hs[1]
  h_small <- hs[length(hs)]

  m_big  <- (f(x0 + h_big)  - f(x0)) / h_big
  m_small <- (f(x0 + h_small) - f(x0)) / h_small

  abline(a = (f(x0) - m_big * x0), b = m_big, col = "gray50", lwd = 2)
  abline(a = (f(x0) - m_small * x0), b = m_small, col = "gray20", lwd = 2)

  legend("topleft",
         legend = c(paste0("secante (h=", h_big, ")"),
                    paste0("secante (h=", h_small, ")")),
         lty = 1, col = c("gray50", "gray20"), bty = "n")
}

