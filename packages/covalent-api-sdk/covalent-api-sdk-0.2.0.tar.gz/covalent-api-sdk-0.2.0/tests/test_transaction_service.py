from covalent import CovalentClient
import pytest
import os



class TestTransactionService:
    
    @pytest.fixture
    def client(self):
        return CovalentClient(os.environ.get('COVALENT_API_KEY'))

    def test_success_for_get_transaction(self, client: CovalentClient):
        res =  client.transaction_service.get_transaction("eth-mainnet", "0xb27a3a3d660b7d679ebbd7065635c8c3613e32eb0ebae24863a6375d73d1a128")
        assert res.error is False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
        assert res.data.items[0].tx_hash == "0xb27a3a3d660b7d679ebbd7065635c8c3613e32eb0ebae24863a6375d73d1a128"
        
            
    def test_incorrect_hash_for_transaction(self, client: CovalentClient):
        res =  client.transaction_service.get_transaction("eth-mainnet", "0xtest")
        assert res.error is True
        assert res.data is None
        assert res.error_code == 400
        assert res.error_message == "Transaction Hash '0xtest' malformed"
    
    def test_success_for_get_transaction_summary(self, client: CovalentClient):
        res =  client.transaction_service.get_transaction_summary("eth-mainnet", "demo.eth")
        assert res.error is False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.address == "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"
        assert len(res.data.items) > 0
    
    def test_incorrect_address_for_get_transaction_summary(self, client: CovalentClient):
        res =  client.transaction_service.get_transaction_summary("eth-mainnet", "0x123")
        assert res.error is True
        assert res.data is None
        assert res.error_code == 400
        assert res.error_message == "Malformed address provided: 0x123"
    
    def test_success_for_transaction_block(self, client: CovalentClient):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 17685920)
        assert res.error is False
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.chain_id == 1
        assert res.data.items[0].block_height == 17685920

    def test_invalid_block_height(self, client: CovalentClient):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 100000000)
        assert res.error is True
        assert res.data is None
        assert res.error_code == 404
        assert res.error_message == "Block not found: chain-height '100000000' has not yet been reached for chain 'eth-mainnet'."
    
    def test_no_logs_for_transaction_block(self, client: CovalentClient):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 17685920, "CAD", True)
        assert res.error is False
        assert res.data.items[0].log_events is None   
    
    
    @pytest.mark.asyncio
    async def test_success_for_get_all_transactions(self, client: CovalentClient):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth"):
            assert res is not None
    
    
    @pytest.mark.asyncio
    async def test_malformed_address(self, client: CovalentClient):
        with pytest.raises(Exception) as exc_info:
            async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "0x1233"):
                assert "An error occured 400 : Malformed address provided: 0x123123" in str(exc_info.value)

    
    @pytest.mark.asyncio
    async def test_quote_currency(self, client: CovalentClient):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth", "CAD"):
            assert res is not None
    
    
    @pytest.mark.asyncio
    async def test_no_logs_for_get_all_transactions(self, client: CovalentClient):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth", "CAD", True):
            assert res.log_events is None
    
    
    
    
        
    
    

