def test_import_redian():
    try:
        import redian_source
        assert hasattr(redian_source, '__version__')
        print(f"Imported redian_source version: {redian_source.__version__}")
    except Exception as e:
        print(f"Import failed: {e}")
        assert False

if __name__ == "__main__":
    test_import_redian() 