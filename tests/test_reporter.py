import pytest
from src.dashboard.reporter import PRISMReporter

def test_report_generation():
    reporter = PRISMReporter()
    
    ring_id = "RING-TEST-001"
    evidence = {
        "confidence": 0.95,
        "hypothesis": "Test Hypothesis",
        "indicators": ["Ind 1", "Ind 2"],
        "exposure": 1000.50
    }
    attribution = {
        "top_partners": {"P1": 10},
        "top_subs": {"S1": 10},
        "is_cross_partner": False,
        "is_cross_sub": False
    }
    
    html = reporter.generate_html_report(ring_id, evidence, attribution)
    
    assert "<!DOCTYPE html>" in html
    assert "RING-TEST-001" in html
    assert "95.0%" in html
    assert "Ind 1" in html
    assert "$1,000.50" in html
