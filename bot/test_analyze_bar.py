import os
import cv2
import numpy as np
import pytest
from analyze_bar import analyze_bar
import glob

# Dynamically collect all PNG files and infer expected state from filename
def collect_test_cases():
    expected_map = {
        "click": "click",
        "wait": "wait"
    }
    cases = []
    for fname in glob.glob("test-cases/*.png"):
        base = os.path.basename(fname)
        for key, state in expected_map.items():
            if base.startswith(key):
                cases.append((fname, state))
                break
    return cases

@pytest.mark.parametrize("filename,expected_state", collect_test_cases())
def test_analyze_bar_states(monkeypatch, filename, expected_state):
    # Patch cv2.imshow, cv2.waitKey, cv2.destroyAllWindows to avoid GUI popups
    monkeypatch.setattr("cv2.imshow", lambda *a, **k: None)
    monkeypatch.setattr("cv2.waitKey", lambda *a, **k: None)
    monkeypatch.setattr("cv2.destroyAllWindows", lambda *a, **k: None)

    # Load image and crop as in main.py
    img = cv2.imread(filename)
    assert img is not None, f"Image {filename} not found"
    top = 123
    left = 575
    height = 24
    width = 755
    crop = img[top:top+height, left:left+width]

    # Get return value
    actual_state = analyze_bar(crop)
    assert expected_state == actual_state, f"Expected: '{expected_state}', Actual: '{actual_state}'"

def test_all_images_report(monkeypatch):
    # Patch cv2.imshow, cv2.waitKey, cv2.destroyAllWindows to avoid GUI popups
    monkeypatch.setattr("cv2.imshow", lambda *a, **k: None)
    monkeypatch.setattr("cv2.waitKey", lambda *a, **k: None)
    monkeypatch.setattr("cv2.destroyAllWindows", lambda *a, **k: None)

    # Map expected states by filename pattern
    expected_map = {
        "click": "click",
        "wait": "wait"
    }

    results = []
    for fname in os.listdir("test-cases"):
        if fname.endswith(".png"):
            full_path = os.path.join("test-cases", fname)
            img = cv2.imread(full_path)
            if img is None:
                continue
            top = 123
            left = 575
            height = 24
            width = 755
            crop = img[top:top+height, left:left+width]
            actual_state = analyze_bar(crop)
            for key, state in expected_map.items():
                if fname.startswith(key):
                    passed = state == actual_state
                    results.append((fname, state, actual_state, passed))
                    break

    # Print summary
    print("\nTest Summary:")
    for fname, expected, actual, passed in results:
        print(f"{fname}: expected '{expected}', actual '{actual}' - {'PASS' if passed else 'FAIL'}")

    # Optionally, assert all passed
    assert all(passed for _, _, _, passed in results), "Some images failed their expected state"
