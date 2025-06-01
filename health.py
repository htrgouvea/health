import argparse
import sys
from health.reader.weight_reader import WeightReader
from health.predictor.weight_predictor import WeightPredictor

def main():
    parser = argparse.ArgumentParser(
        description="Health insights CLI - Extract and predict health data."
    )

    parser.add_argument('--extract', choices=['weight'], help='Extract health data (e.g., weight)')
    parser.add_argument('--predict', choices=['weight'], help='Predict health data (e.g., weight)')
    parser.add_argument('--value', type=int, help='Days to predict into the future (default: 7)')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.extract == 'weight':
        reader = WeightReader('export.xml')
        reader.extract_to_csv('data/weight.csv')

    if args.predict == 'weight':
        days = args.value if args.value else 7
        predictor = WeightPredictor('data/weight.csv')
        predictor.predict(
            output_csv='output/weight_forecast.csv',
            output_plot='plots/weight_forecast.png',
            days_ahead=days
        )

if __name__ == '__main__':
    main()