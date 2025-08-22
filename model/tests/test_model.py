import unittest

import ml_service


# 💡 NOTE Run test with:
# - python3 -m unittest -vvv tests.test_model
# - python3 tests/test_model.py
class TestMLService(unittest.TestCase):
    def test_predict(self):
        ml_service.settings.UPLOAD_FOLDER = "tests"
        class_name, pred_probability = ml_service.predict("dog.jpeg")
        self.assertEqual(class_name, "Eskimo_dog")
        self.assertAlmostEqual(pred_probability, 0.9346, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
