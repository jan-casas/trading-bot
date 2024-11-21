from flask import Flask, request, jsonify
from strategy_manager import StrategyManager
from main import scheduler
from config.config import STRATEGY_PARAMETERS

app = Flask(__name__)
strategy_manager = StrategyManager()
strategy_manager.load_strategies()

@app.route('/strategies', methods=['GET'])
def list_strategies():
    strategies = [strategy.get_name() for strategy in strategy_manager.get_strategies()]
    return jsonify(strategies)

@app.route('/strategies/<strategy_name>/schedule', methods=['POST'])
def update_strategy_schedule(strategy_name):
    data = request.get_json()
    new_schedule = data.get('schedule')
    if new_schedule:
        # Update schedule in scheduler
        scheduler.reschedule_job(strategy_name, trigger='cron', **new_schedule)
        # Update schedule in configuration
        STRATEGY_PARAMETERS[strategy_name]['schedule'] = new_schedule
        return jsonify({'message': f'Schedule updated for {strategy_name}'})
    else:
        return jsonify({'error': 'No schedule provided'}), 400

@app.route('/strategies/<strategy_name>/enable', methods=['POST'])
def enable_strategy(strategy_name):
    # Enable the strategy
    success = strategy_manager.enable_strategy(strategy_name)
    if success:
        return jsonify({'message': f'Strategy {strategy_name} enabled'})
    else:
        return jsonify({'error': f'Unable to enable strategy {strategy_name}'}), 400

@app.route('/strategies/<strategy_name>/disable', methods=['POST'])
def disable_strategy(strategy_name):
    # Disable the strategy
    success = strategy_manager.disable_strategy(strategy_name)
    if success:
        return jsonify({'message': f'Strategy {strategy_name} disabled'})
    else:
        return jsonify({'error': f'Unable to disable strategy {strategy_name}'}), 400


@app.route('/strategies/<strategy_name>/params', methods=['POST'])
def update_strategy_params(strategy_name):
    data = request.get_json()
    new_params = data.get('params')
    if new_params:
        # Update strategy parameters
        success = strategy_manager.update_strategy_params(strategy_name, new_params)
        if success:
            return jsonify({'message': f'Parameters updated for {strategy_name}'})
        else:
            return jsonify({'error': f'Strategy {strategy_name} not found'}), 404
    else:
        return jsonify({'error': 'No parameters provided'}), 400


if __name__ == '__main__':
    app.run(port=5000)