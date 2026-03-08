// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RiskScore {
    mapping(address => uint256) public riskScores;

    event RiskScoreUpdated(address indexed user, uint256 score);

    function setRiskScore(address user, uint256 score) public {
        riskScores[user] = score;
        emit RiskScoreUpdated(user, score);
    }

    function getRiskScore(address user) public view returns (uint256) {
        return riskScores[user];
    }
}