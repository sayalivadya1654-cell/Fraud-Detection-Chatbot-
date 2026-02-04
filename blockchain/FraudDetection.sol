// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudDetection {
    struct Result {
        string txnId;
        string status;
        uint256 timestamp;
    }

    Result[] private results;

    event ResultStored(string txnId, string status, uint256 timestamp);

    function storeResult(string memory _txnId, string memory _status) public {
        results.push(Result({
            txnId: _txnId,
            status: _status,
            timestamp: block.timestamp
        }));
        emit ResultStored(_txnId, _status, block.timestamp);
    }

    function getResultCount() public view returns (uint256) {
        return results.length;
    }

    function getResultAt(uint256 index) public view returns (string memory, string memory, uint256) {
        require(index < results.length, "Index out of bounds");
        Result storage res = results[index];
        return (res.txnId, res.status, res.timestamp);
    }
}
