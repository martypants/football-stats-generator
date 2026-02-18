"""
Integration tests for the football stats generator
"""
import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from aggregator import StatsAggregator

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.aggregator = StatsAggregator()
    
    def test_end_to_end_scraping_workflow(self):
        """Test complete workflow from scraping to CSV export"""
        # Aggregate multiple data points
        self.aggregator.aggregate_player_stats("Kylian Mbappé", "Real Madrid")
        self.aggregator.aggregate_player_stats("Vinícius Júnior", "Real Madrid")
        self.aggregator.aggregate_team_stats("Real Madrid")
        self.aggregator.aggregate_match_stats("Real Madrid", "Manchester City")
        
        # Verify data was collected
        data = self.aggregator.get_aggregated_data()
        self.assertEqual(len(data), 4)
        
        # Test CSV export
        csv_file = self.aggregator.export_to_csv("test_integration.csv")
        self.assertIsNotNone(csv_file)
        
        # Verify CSV file was created
        self.assertTrue(os.path.exists(csv_file))
        
        # Cleanup
        if os.path.exists(csv_file):
            os.remove(csv_file)
    
    def test_multiple_team_aggregation(self):
        """Test aggregating stats for multiple teams"""
        teams = ["Real Madrid", "Manchester City", "Bayern Munich"]
        
        for team in teams:
            self.aggregator.aggregate_team_stats(team)
        
        data = self.aggregator.get_aggregated_data()
        self.assertEqual(len(data), len(teams))
    
    def test_data_structure_consistency(self):
        """Test that all aggregated data follows consistent structure"""
        self.aggregator.aggregate_player_stats("Test Player", "Test Team")
        data = self.aggregator.get_aggregated_data()
        
        for item in data:
            self.assertIn("timestamp", item)
            self.assertIn("sources", item)
            self.assertIn("stats", item)

if __name__ == '__main__':
    unittest.main()