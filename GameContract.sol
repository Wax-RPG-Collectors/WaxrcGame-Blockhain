// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameContract {
    struct Game {
        string name;
        string logo;
        string url;
        uint256 timePlayed;
        uint256 startTime;
        bool exists;
    }

    mapping(string => Game) public games;

    function createGame(string memory gameId, string memory name, string memory logo, string memory url) public {
        require(!games[gameId].exists, "Game with this ID already exists.");
        games[gameId] = Game(name, logo, url, 0, block.timestamp, true);
    }

    function updateGameTime(string memory gameId, uint256 timePlayed) public {
        require(games[gameId].exists, "Game not found.");
        games[gameId].timePlayed += timePlayed;
    }

    function getTimePlayed(string memory gameId) public view returns (uint256) {
        require(games[gameId].exists, "Game not found.");
        return games[gameId].timePlayed;
    }

    function getGameDetails(string memory gameId) public view returns (string memory, string memory, string memory, uint256, uint256) {
        require(games[gameId].exists, "Game not found.");
        Game memory game = games[gameId];
        return (game.name, game.logo, game.url, game.timePlayed, game.startTime);
    }
}