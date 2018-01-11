// *********************************************
// Interface: Displaying popups after pagechange
// *********************************************

var gError = "";
var gMessage = "";

$(document).on( "pagechange", function() {
    if (gError !== "") {
        showError("Error",gError);
        gError = "";
    }

    if (gMessage !== "") {
        showMessage(gMessage);
        gMessage = "";
    } else if ($.mobile.activePage.attr("id")=="PageMainMenu" && Math.random() < 0.05) {
        quotes = [
            ["A word to the wise ain't necessary - it's the stupid ones that need the advice.","Bill Cosby"],
            ["People who think they know everything are a great annoyance to those of us who do.","Isaac Asimov"],
            ["Between two evils, I always pick the one I never tried before.","Mae West"],
            ["A woman's mind is cleaner than a man's: She changes it more often.","Oliver Herford"],
            ["Housework can't kill you, but why take a chance?","Phyllis Diller"],
            ["All generalizations are false, including this one.","Mark Twain"],
            ["I cook with wine, sometimes I even add it to the food.","W. C. Fields"],
            ["Do not worry about avoiding temptation. As you grow older it will avoid you.","Joey Adams"],
            ["I love deadlines. I like the whooshing sound they make as they fly by.","Douglas Adams"],
            ["Before I refuse to take your questions, I have an opening statement.","Ronald Reagan"],
            ["I haven't spoken to my wife in years. I didn't want to interrupt her.","Rodney Dangerfield"],
            ["Life is hard. After all, it kills you.","Katharine Hepburn"],
            ["I saw a woman wearing a sweatshirt with Guess on it. I said, Thyroid problem?","Arnold Schwarzenegger"],
            ["There cannot be a crisis next week. My schedule is already full.","Henry A. Kissinger"],
            ["I'm sorry, if you were right, I'd agree with you.","Robin Williams"],
            ["Roses are red, violets are blue, I'm schizophrenic, and so am I.","Oscar Levant"],
            ["What's another word for Thesaurus?","Steven Wright"],
            ["A committee is a group that keeps minutes and loses hours.","Milton Berle"],
            ["I hate housework! You make the beds, you do the dishes and six months later you have to start all over again.","Joan Rivers"],
            ["Every man's dream is to be able to sink into the arms of a woman without also falling into her hands.","Jerry Lewis"],
            ["What contemptible scoundrel has stolen the cork to my lunch?","W. Clement Stone"],
            ["TV is chewing gum for the eyes.","Frank Lloyd Wright"]
        ];
        var index = Math.floor(Math.random()*quotes.length);
        showMessage(quotes[index][0]+"<br/>&mdash;"+quotes[index][1]);
    }
});

// **************************
// Interface: Display message
// **************************

var messageTimeout = null;
function showMessage(text) {
    var currentPageID = $.mobile.activePage.attr('id');
    var messageDivID = currentPageID + "-Message";
    var messageDiv = $("#"+messageDivID);

    messageDiv.html("<p>"+text+"</p>");
    if (messageTimeout !== null) clearTimeout(messageTimeout);
    messageDiv.show("slow");
    messageTimeout = setTimeout(function() {messageDiv.hide("slow");}, 10000);
}

// ************************
// Interface: Display error
// ************************

function showError(title, text) {
    var currentPageID = $.mobile.activePage.attr('id');
    var errorPopupID = currentPageID + "-ErrorPopup";
    var errorPopupTextID = currentPageID + "-ErrorPopupText";
    var errorPopupTitleID = currentPageID + "-ErrorPopupTitle";
    var errorPopup = $("#"+errorPopupID);
    var errorPopupText = $("#"+errorPopupTextID);
    var errorPopupTitle = $("#"+errorPopupTitleID);

    errorPopupText.empty();
    errorPopupTitle.html(title);
    errorPopupText.html("<p>"+text+"</p>");
    errorPopup.popup("open");
}
