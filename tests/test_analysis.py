from src.analysis import analyze_sentiments

def test_analyze_empty():
    out = analyze_sentiments([])
    assert out == []
