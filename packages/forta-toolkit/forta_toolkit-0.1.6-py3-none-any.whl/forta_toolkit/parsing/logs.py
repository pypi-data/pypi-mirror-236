"""Format blockchain logs."""

import forta_agent.transaction_event

import forta_toolkit.parsing.address

# TRANSACTION LOGS ############################################################

def parse_transaction_data(log: forta_agent.transaction_event.TransactionEvent, get_code: callable) -> dict:
    """Extract and format all the required data."""
    __data = {
        'sender': forta_toolkit.parsing.address.format_with_checksum(getattr(log.transaction, 'from_', '')),
        'recipient': forta_toolkit.parsing.address.format_with_checksum(getattr(log.transaction, 'to', '')),
        'data': log.transaction.data,
        'bytecode': ''}
    # contract creation
    if not __data['recipient']:
        __data['bytecode'] = __data['data'] # use creation bytecode which contains runtime bytecode
    # exclude transactions that are not involving a contract
    if (len(__data['data']) > 2): # counting the prefix
        __data['bytecode'] = get_code(__data['recipient']).hex()
    return __data
