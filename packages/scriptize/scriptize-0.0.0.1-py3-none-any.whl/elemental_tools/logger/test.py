from elemental_tools.logger import Logger

logger = Logger('log', 'me', './path/to/log')

for e in range(10):
	logger.log('info', 'test message')
