FOOTER='No Evidence Docket, no empirical SOTA claim. Autonomous evidence production is allowed; autonomous claim promotion is not.'
CLAIM_BOUNDARY='This hub records bounded Evidence Docket experiments. It does not claim achieved AGI, ASI, empirical SOTA, safe autonomy, real-world certification, guaranteed economic return, or civilization-scale capability. Stronger claims require independent replay, official public benchmarks, cost/safety review, delayed outcomes, and external audit.'

def page(title,body):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <link rel="stylesheet" href="/agialpha-first-real-loop/assets/app.css" />
</head>
<body class="mission-control">
  <header class="topnav">
    <a class="brand" href="/agialpha-first-real-loop/">AGI ALPHA Evidence Mission Control</a>
    <nav>
      <a href="/agialpha-first-real-loop/experiments/">Experiments</a>
      <a href="/agialpha-first-real-loop/workflows/">Workflows</a>
      <a href="/agialpha-first-real-loop/runs/">Runs</a>
      <a href="/agialpha-first-real-loop/launchpad/">Launchpad</a>
    </nav>
  </header>
  <main class="container">
    <section class="panel hero">
      <h1>{title}</h1>
      {body}
    </section>
  </main>
  <footer class="footer">{FOOTER}</footer>
  <script src="/agialpha-first-real-loop/assets/app.js"></script>
</body>
</html>"""
