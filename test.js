var request = require('request');

var domain = '{url}';

var options = {
    'method': 'GET',
    'url': 'https://www.rdap.net/domain/' + domain
};

request(options, function(error, response) {
    if (error) throw new Error(error);
    var newBody = JSON.parse(response.body);
    var expDate = newBody.events[1].eventDate;
    var newExp = Date.parse(expDate);

    var now = Date.now();
    var daysToExp = (newExp - now) / 86400000;

    $util.insights.set("checkedDomain", domain);
    $util.insights.set("domainExpirationDate", newExp);
    $util.insights.set("daysToExpiration", daysToExp);

    console.log(expDate + '\n' + newExp + '\n' + now + '\n' + daysToExp);
});
