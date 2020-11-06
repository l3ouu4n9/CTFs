// Loading of the Slot Machine
const casino1 = document.querySelector('#casino1');
const casino2 = document.querySelector('#casino2');
const casino3 = document.querySelector('#casino3');
let ethereumSlotMachine = null;

function updateContractBalance() {
  web3.eth.getBalance(smartcontract.to, function(error, result) {
    if (!error) {
      document.getElementById("scBalance").innerHTML = web3.utils.fromWei(result, 'ether');
    } else {
      console.log('Error: ', error);
    }
  })
}

const mCasino1 = new SlotMachine(casino1, {
  active: 0,
  delay: 500
});
const mCasino2 = new SlotMachine(casino2, {
  active: 0,
  delay: 500
});
const mCasino3 = new SlotMachine(casino3, {
  active: 0,
  delay: 500
});

let digit1 = "0";
let digit2 = "0";
let digit3 = "0";
let totalDigit = "000";

function loadEthereum() {

  console.log("CASINO: Loading Ethereum Context");

  ethereum.enable()
    .then(function(accounts) {
      smartcontract.from = accounts[0];

      if (ethereum.networkVersion != smartcontract.networkId) {
        $('#infoModalText').html("<p class='modal-body slotDiplayContentSmall'>Don't forget to switch to the ROPSTEN Network and to get some ETHER using the Faucet at https://faucet.ropsten.be/</p>");

        $('#infoModal').modal({
          show: true,
          focus: true,
          keyboard: true,
          backdrop: 'static'
        });
      } else {
        ethereum.enable()
          .then(function(accounts) {
            playerAddress = accounts[0];

            if (ethereum.networkVersion != smartcontract.networkId) {
              $('#infoModalText').html("<p class='modal-body slotDiplayContentSmall'>Don't forget to switch to the ROPSTEN Network and to get some ETHER using the Faucet at https://faucet.ropsten.be/</p><p class='modal-body slotDiplayContentSmall'> Don't forget to refersh the page, when you are done!</p>");

              $('#infoModal').modal({
                show: true,
                focus: true,
                keyboard: true,
                backdrop: 'static'
              });
            } else {
              smartcontract.from = accounts[0];
              web3 = new Web3(window['ethereum']);
              console.log("Web3.js version " + web3.version);
              updateContractBalance();

              window.setInterval(function() {
                updateContractBalance();
              }, 5000);

              ethereumSlotMachine = new web3.eth.Contract(smartcontract.abi, smartcontract.to);
              web3.eth.getBlockNumber().then(function(block) {
                ethereumSlotMachine.events.BetResult({
                  filter: {bidder: smartcontract.from}, // Using an array means OR: e.g. 20 or 23
                  fromBlock: block-1
                })
                .on('data', function(event){
                  callbackBetResult(event, uuid()); // same results as the optional callback above
                })
              })

            }
          })
      }
    })
    .catch(function(error) {

      $('#infoModalText').html("<p class='modal-body slotDiplayContentSmall'>You must logged in on MetaMask and accept the connection request before you can start playing!</p><p class='modal-body slotDiplayContentSmall'> Don't forget to refersh the page, when you are done!</p>");

      $('#infoModal').modal({
        show: true,
        focus: true,
        keyboard: true,
        backdrop: 'static'
      });
    })
}

// Loading on Windows ready

jQuery(function() {

  // Run background video
  jQuery("#bgndVideo").YTPlayer();

  // Initial button state
  jQuery("#casinoBet").prop('disabled', true);

  // Detected Etherum Provider
  if (typeof window.ethereum !== 'undefined') {
    const provider = window['ethereum'];

    ethereum.autoRefreshOnNetworkChange = false;

    ethereum.on('networkChanged', function(chainId) {
      location.reload();
    })

    loadEthereum();

  } else {

    $('#infoModalText').html(
      "<p class='modal-body slotDiplayContentSmall'>You should install the MetaMask extension in your browser to start playing!</p><p class='modal-body slotDiplayContentSmall'> Don't forget to refersh the page, when you are done!</p>"
    );

    $('#infoModal').modal({
      show: true,
      focus: true,
      keyboard: true,
      backdrop: 'static'
    });
  }

});

// Upon click from Shuffle
$("#casinoShuffle").on('click', function(event) {

  mCasino1.shuffle(1, onComplete1);
  mCasino2.shuffle(2, onComplete2);
  mCasino3.shuffle(3, onComplete3);

  $("#casinoShuffle").prop('disabled', true);
  $("#casinoBet").prop('disabled', true);
})

function onComplete1(active) {
  digit1 = active.toString();
}

function onComplete2(active) {
  digit2 = active.toString();
}

function onComplete3(active) {
  digit3 = active.toString();
  totalDigit = digit1 + digit2 + digit3;
  $("#casinoShuffle").prop('disabled', false);
  $("#casinoBet").prop('disabled', false);
}

// Upom click on Bet
$("#casinoBet").on('click', function(event) {

  // Init while loading
  $("#casinoShuffle").prop('disabled', true);
  $("#casinoBet").prop('disabled', true);

  $("#serverStatus").html("<i class='far fa-clock fa-2x'></i></i><span class='slotDiplayContentSmall'> LOADING - WAITING FOR BET RESULT</span>");

  // Start invocation of smart smartcontract play() method
  const transactionObject = {
    from: smartcontract.from,
    value: web3.utils.toWei('100', 'finney')
  };

  ethereumSlotMachine.methods.play(Number(totalDigit)).send(transactionObject, function(error, result){ // do something with error checking/result here });)
    if (error) {
      $("#casinoShuffle").prop('disabled', false);
      $("#casinoBet").prop('disabled', false);
      $("#serverStatus").html("<i class='far fa-pause-circle fa-2x'></i><span class='slotDiplayContentSmall'> IDLE - WAITING FOR BET</span>");
    }
  });

})

// Callback Event
async function callbackBetResult(eventObj, uuid) {

  let bidder = eventObj.returnValues.bidder;
  let success = eventObj.returnValues.response;
  if(bidder.toUpperCase() === smartcontract.from.toUpperCase()){
    if (success){
      var challenge = uuid;
      var accounts = await web3.eth.getAccounts();
      var signature = await web3.eth.personal.sign(challenge, accounts[0]);
      verifyFlag(bidder, uuid, signature);

    }else{
      $("#casinoShuffle").prop('disabled', false);
      $("#casinoBet").prop('disabled', false);
      $("#serverStatus").html("<i class='fas fa-bomb fa-2x'></i></i><span class='slotDiplayContentSmall'> WRONG NUMBER SUBMITTED!</span>");
    }
  }
}

function verifyFlag(bidder, uuid, signature){

  $.get(
    "/bet/verify",
    {
       address: bidder,
       message: uuid,
       signature: signature
    },
    function(data) {
       if (data != "FAILURE"){
         $("#casinoShuffle").prop('disabled', false);
         $("#casinoBet").prop('disabled', false);
         $("#serverStatus").html("<i class='far fa-flag fa-2x'></i></i><span class='slotDiplayContentSmall' style='margin-left:5px'>" + data + "</span>");
       }else{
         $("#casinoShuffle").prop('disabled', false);
         $("#casinoBet").prop('disabled', false);
         $("#serverStatus").html("<i class='fas fa-bomb fa-2x'></i></i><span class='slotDiplayContentSmall'> WRONG NUMBER SUBMITTED!</span>");
       }
   }
 );
}