"""
Unit tests for the football stats scraper
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from scrapers.espn_scraper import ESPNScraper
from scrapers.fbref_scraper import FBrefScraper
from scrapers.transfermarkt_scraper import TransfermarktScraper
from scrapers.understat_scraper import UnderstatScraper
from aggregator import StatsAggregator

class TestESPNScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = ESPNScraper()
    
    def test_player_stats_structure(self):
        """Test that ESPN scraper returns correct data structure"""
        result = self.scraper.scrape_player_stats("Test Player")
        self.assertIsNotNone(result)
        self.assertIn("player_name", result)
        self.assertIn("source", result)
        self.assertEqual(result["source"], "ESPN")
        self.assertIn("shots_on_target", result)
        self.assertIn("xg", result)
        self.assertIn("possession_pct", result)
        self.assertIn("corners", result)
        self.assertIn("chances_created", result)
    
    def test_team_stats_structure(self):
        """Test that ESPN team stats returns correct structure"""
        result = self.scraper.scrape_team_stats("Test Team")
        self.assertIsNotNone(result)
        self.assertIn("team_name", result)
        self.assertIn("source", result)
        self.assertEqual(result["source"], "ESPN")

class TestFBrefScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = FBrefScraper()
    
    def test_player_stats_structure(self):
        """Test that FBref scraper returns correct data structure"""
        result = self.scraper.scrape_player_stats("Test Player")
        self.assertIsNotNone(result)
        self.assertIn("player_name", result)
        self.assertIn("source", result)
        self.assertEqual(result["source"], "FBref")
        self.assertIn("xg", result)
        self.assertIn("season", result)

class TestTransfermarktScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = TransfermarktScraper()
    
    def test_player_stats_structure(self):
        """Test that Transfermarkt scraper returns correct data structure"""
        result = self.scraper.scrape_player_stats("Test Player", "Test Team")
        self.assertIsNotNone(result)
        self.assertIn("player_name", result)
        self.assertIn("source", result)
        self.assertEqual(result["source"], "Transfermarkt")
        self.assertIn("market_value", result)

class TestUnderstatScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = UnderstatScraper()
    
    def test_player_stats_structure(self):
        """Test that Understat scraper returns correct data structure"""
        result = self.scraper.scrape_player_stats("Test Player")
        self.assertIsNotNone(result)
        self.assertIn("source", result)
        self.assertEqual(result["source"], "Understat")
        self.assertIn("xg_per_shot", result)
    
    def test_match_stats_structure(self):
        """Test that Understat match stats returns correct structure"""
        result = self.scraper.scrape_match_stats("Team A", "Team B")
        self.assertIsNotNone(result)
        self.assertIn("team1", result)
        self.assertIn("team2", result)
        self.assertIn("team1_xg", result)
        self.assertIn("team2_xg", result)

class TestStatsAggregator(unittest.TestCase):
    def setUp(self):
        self.aggregator = StatsAggregator()
    
    def test_aggregate_player_stats(self):
        """Test player stats aggregation"""
        result = self.aggregator.aggregate_player_stats("Mbappé", "Real Madrid")
        self.assertIsNotNone(result)
        self.assertIn("player_name", result)
        self.assertIn("team_name", result)
        self.assertIn("stats", result)
        self.assertIn("sources", result)
    
    def test_aggregate_team_stats(self):
        """Test team stats aggregation"""
        result = self.aggregator.aggregate_team_stats("Real Madrid")
        self.assertIsNotNone(result)
        self.assertIn("team_name", result)
        self.assertIn("league", result)
        self.assertIn("stats", result)
    
    def test_aggregate_match_stats(self):
        """Test match stats aggregation"""
        result = self.aggregator.aggregate_match_stats("Real Madrid", "Manchester City")
        self.assertIsNotNone(result)
        self.assertIn("team1", result)
        self.assertIn("team2", result)
    
    def test_get_aggregated_data(self):
        """Test retrieving aggregated data"""
        self.aggregator.aggregate_player_stats("Test Player", "Test Team")
        data = self.aggregator.get_aggregated_data()
        self.assertGreater(len(data), 0)
    
    def test_export_to_csv(self):
        """Test CSV export functionality"""
        self.aggregator.aggregate_player_stats("Test Player", "Test Team")
        result = self.aggregator.export_to_csv("test_output.csv")
        self.assertIsNotNone(result)
        # Cleanup
        import os
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")

if __name__ == '__main__':
    unittest.main()