import unittest
import src.main


class AudioBatchDownload(unittest.TestCase):
    def test_get_domain_from_url(self):
        urls = [
            "https://highered.mheducation.com/sites/0078025141/student_view0/workbook_recordings.html",
            "https://www.john-scrivo.de/lessons.htm",
        ]
        domains = [src.main.get_domain_from_url(url) for url in urls]

        self.assertListEqual(
            domains,
            [
                "https://highered.mheducation.com/",
                "https://www.john-scrivo.de/",
            ],
        )


if __name__ == "__main__":
    unittest.main()
