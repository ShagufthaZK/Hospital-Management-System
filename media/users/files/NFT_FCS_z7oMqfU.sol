// Used OpenZeppelin's open source framework to build the basic smart contract. Used the ERC-721 standard of tokens
// Feautres opted were Mintabe, Auto Increment Ids, Enumerable and URI storage. Used Remix - an Etherum IDE to implement 
// and deplot this smart contract ahead. A few changes were made, declared a limit of 10,000 mints allowed. The contract
// was then compiled on the IDE. Created an Alchemy and MetaMask account to deploy the contract.

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9; //version of solidity used in our contract


//importing libraries
import "@openzeppelin/contracts@4.8.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.8.0/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts@4.8.0/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.8.0/utils/Counters.sol";

//Declaring the contract named 'PToken' here, inherting the four classes - ERC721, ERC721Enumerable,
//ERC721URIStorage and Ownable
contract PToken is ERC721, ERC721Enumerable, ERC721URIStorage {
    using Counters for Counters.Counter; //Initializing the counters library

    Counters.Counter private _tokenIdCounter; //Creating a private counter varuable named _tokenIdCounter

    uint256 LIMIT=10000; // constant declared to keep a cap on the limit of NFTs we can mint
    constructor() ERC721("PToken", "PRV") {} //Counstructor creates an Instance of the Smart Contract, since
    //we are inheriting from ERC721 token standard, we're assigning a name and symbol of our smartphone


    //Minting is the action of writing new content on a blockchain
    function safeMint(address to, string memory uri) public  { //Creating a public function named safeMint, parameters required are
                                                                        //address of a wallet we want to send the NFT to, and the uri
        uint256 tokenId = _tokenIdCounter.current(); //stores the current token ID that _tokenIdCounter is keeping track of
        require(tokenId <= LIMIT, "NFTs limit reached!"); //when tokenId surpasses the limit, it'll stop
        _tokenIdCounter.increment(); // Incrementing the number for next NFTs
        _safeMint(to, tokenId); // calling the _safeMint function, passing address and tokenId as arguments. Creates a new entry on the blockchain.
        _setTokenURI(tokenId, uri); // assigning TokenURI to our NFT
    }

    // The following functions are overrides required by Solidity.

    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
