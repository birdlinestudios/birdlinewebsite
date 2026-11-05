// The 404 page, in the site's own hero styling (app/globals.css).
export default function NotFound() {
  return (
    <main>
      <section className="hero hero--page on-dark" id="top" style={{ paddingBottom: 96 }}>
        <div className="wrap hero-copy">
          <span className="eyebrow">404</span>
          <h1 className="h2">That page flew the coop.</h1>
          <p className="sub" style={{ color: "rgba(255,255,255,.78)" }}>
            The address may have changed, or the link was wrong. Everything we make is a click away.
          </p>
          <div className="cta-row" style={{ marginTop: 28 }}>
            <a className="btn btn--light" href="/">Back to the homepage</a>
            <a className="btn btn--ghost" href="/work">See the work</a>
          </div>
        </div>
      </section>
    </main>
  );
}
