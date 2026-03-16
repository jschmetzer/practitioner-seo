"""Shared test fixtures for Practitioner SEO tests."""

import pytest

from practitioner_seo.config import Config, GSCConfig


SAMPLE_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Best Hand Planes for Every Skill Level (2026)</title>
    <meta name="description" content="Professional furniture maker Sarah Chen reviews the best hand planes for beginners through advanced woodworkers.">
    <link rel="canonical" href="https://benchcraftworkshop.com/best-hand-planes/">
    <meta property="og:title" content="Best Hand Planes">
    <meta property="og:image" content="https://benchcraftworkshop.com/images/hand-planes.jpg">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Best Hand Planes for Every Skill Level",
        "author": {
            "@type": "Person",
            "@id": "https://benchcraftworkshop.com/#author",
            "name": "Sarah Chen"
        },
        "dateModified": "2026-01-15"
    }
    </script>
</head>
<body>
    <nav>
        <a href="https://benchcraftworkshop.com/">Home</a>
        <a href="https://benchcraftworkshop.com/about/">About</a>
    </nav>
    <h1>Best Hand Planes for Every Skill Level</h1>
    <p>The No. 4 smoothing plane is the single most useful hand plane you can own.
    At 9-3/4 inches long with a 2-inch blade, it handles everything from rough
    dimensioning to final smoothing on boards under 18 inches. I have used dozens
    of hand planes over 20 years of professional furniture making, and the No. 4
    remains the workhorse of every shop I have built.</p>
    <h2>What Makes a Good Hand Plane</h2>
    <p>A good hand plane needs three things: a flat sole, a well-bedded blade,
    and comfortable handles. Everything else is preference.</p>
    <a href="https://benchcraftworkshop.com/hand-plane-sharpening/">sharpening guide</a>
    <a href="http://benchcraftworkshop.com/smoothing-plane-vs-jack-plane/">smoothing vs jack</a>
    <h2>Best Hand Planes by Type</h2>
    <p>Here are the planes I recommend for each category.</p>
    <img src="/images/no4.jpg" alt="Lie-Nielsen No. 4 smoothing plane">
    <img src="/images/block.jpg" alt="">
    <img src="/images/jointer.jpg">
    <h2>FAQ</h2>
    <h3>What hand plane should a beginner buy first?</h3>
    <p>A No. 4 smoothing plane from Stanley or a vintage Bailey.</p>
    <a href="https://amzn.to/example123">Stanley No. 4 on Amazon</a>
</body>
</html>"""


@pytest.fixture
def sample_html():
    """Return sample HTML for testing page extraction."""
    return SAMPLE_HTML


@pytest.fixture
def sample_config():
    """Return a Config object with no API keys set (for degradation tests)."""
    return Config()


@pytest.fixture
def sample_config_with_serpapi():
    """Return a Config with a fake SerpAPI key."""
    return Config(serpapi_key="test-serpapi-key-12345")


@pytest.fixture
def sample_config_with_all():
    """Return a Config with all keys set (fake values)."""
    return Config(
        serpapi_key="test-serpapi-key",
        pagespeed_key="test-psi-key",
        gsc=GSCConfig(
            auth_method="service_account",
            service_account_file="/tmp/fake-sa.json",
        ),
    )
