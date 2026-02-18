"""
Main script to run the football stats scraper
Usage: python main.py
"""
import logging
from aggregator import StatsAggregator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main execution function
    """
    logger.info("Starting Football Stats Generator")
    
    # Initialize aggregator
    aggregator = StatsAggregator()
    
    # Example: Scrape stats for Champions League match
    logger.info("Scraping Champions League player statistics...")
    
    # Example players - Replace with actual players for tonight's match
    players = [
        {"name": "Kylian Mbappé", "team": "Real Madrid"},
        {"name": "Vinícius Júnior", "team": "Real Madrid"},
        {"name": "Jude Bellingham", "team": "Real Madrid"},
    ]
    
    # Aggregate player stats
    for player in players:
        logger.info(f"Processing {player['name']} from {player['team']}")
        aggregator.aggregate_player_stats(player['name'], player['team'])
    
    # Aggregate team stats
    teams = ["Real Madrid", "Manchester City", "Bayern Munich"]
    for team in teams:
        logger.info(f"Processing team stats for {team}")
        aggregator.aggregate_team_stats(team, league="champions-league")
    
    # Aggregate match stats
    logger.info("Processing match statistics")
    aggregator.aggregate_match_stats("Real Madrid", "Manchester City", league="champions-league")
    
    # Export data to CSV
    csv_filename = "champions_league_stats.csv"
    logger.info(f"Exporting data to {csv_filename}")
    aggregator.export_to_csv(csv_filename)
    
    logger.info("Football Stats Generator completed successfully")

if __name__ == "__main__":
    main()