$(document).ready(onReady);

var MAX_BREAKS = 10;
var DECIMALS = 2;
var breaks = 0;
var timer;

function onReady() {
	console.log('ready');
	doBreaksButtons();
	doSlider();
	doPhases();
	updateStatus(true);

	$("#soundCheckbox").click(function() {
		if (this.checked) {
			myJSON("/api/settings?sound=play");
		}
		else {
			myJSON("/api/settings?sound=mute");
		}
	});
	$("#backlightCheckbox").click(function() {
		if (this.checked) {
			myJSON("/api/settings?backlight=enable");
		}
		else {
			myJSON("/api/settings?backlight=disable");
		}
	});
}

function doPhases(mode) {
	function connectRadioButton(name, url) {
		if (mode != null) {
			if (mode == url.toUpperCase()) {
				$(name).prop("checked", true);
			}
		}
		else {
			$(name).change(function() {
				if (this.checked) {
					myJSON("/api/brew?mode=" + url);
				}
			});
		}
	};
	connectRadioButton("#closePhase", "close");
	connectRadioButton("#openPhase", "open");
	connectRadioButton("#cleaningPhase", "cleaing");
	connectRadioButton("#mashingPhase", "mashing");
	connectRadioButton("#filteringTurnAroundPhase", "filtering_turn_around");
	connectRadioButton("#filteringAddWaterPhase", "filtering_add_water");
	connectRadioButton("#filteringPlewingPhase", "filtering_plewing");
	connectRadioButton("#coolingPhase", "cooling");
}

function updateStatus(setNext) {
	myJSON('/api/status', function(json) {
		if (json.STATUS == 0) {
			$("#heater").text(json.DATA.DEVICES.HEATER);
			$("#heap").text(json.DATA.NODE.HEAP);
			$("#uptime").text(formatSeconds(json.DATA.NODE.UPTIME));
			$("#voltage").text(json.DATA.NODE.VOLTAGE);
			$("#wifi_ssid").text(json.DATA.NODE.WIFI.SSID);
			$("#wifi_signal").text(json.DATA.NODE.WIFI.SIGNAL);
			$("#wifi_mac").text(json.DATA.NODE.WIFI.MAC);

			$("#expectedTemperatureValue").text(json.DATA.BREW.TEMP);
			$("#expectedTemperatureInput").slider('setValue', json.DATA.BREW.TEMP, true);
			$("#pumpValue").text(json.DATA.DEVICES.PUMP);
			$("#pumpInput").slider('setValue', json.DATA.DEVICES.PUMP, true);
			$("#fanValue").text(json.DATA.DEVICES.FAN);
			$("#fanInput").slider('setValue', json.DATA.DEVICES.FAN, true);

			externalTemperatures = json.DATA.TEMP.EXTERNAL.map(function (t) { return t.toFixed(DECIMALS).toString() + "&#x2103;"; })
			$("#averageExternalTemperature").text(json.DATA.TEMP.AVERAGE_EXTERNAL.toFixed(DECIMALS));
			$("#externalTemperatures").html(externalTemperatures.join(', '));
			$("#internalTemperature").text(json.DATA.TEMP.INTERNAL.toFixed(DECIMALS));

			isStarted = json.DATA.BREW.STARTED;
			$("#editBreaks").attr("disabled", isStarted || !$("#saveBreaks").is(":disabled"));
			$("#startBrew").attr("disabled", isStarted || !$("#saveBreaks").is(":disabled"));
			$("#stopBrew").attr("disabled", !isStarted);
			$("#expectedTemperatureInput").slider((isStarted ? 'disable' : 'enable'));
			$("#soundCheckbox").prop("checked", json.DATA.SETTINGS.SOUND);
			$("#backlightCheckbox").prop("checked", json.DATA.SETTINGS.BACKLIGHT);
			if ($("#saveBreaks").is(":disabled") && !jQuery.isEmptyObject(json.DATA.BREW.BREAKS)) {
				breaks = json.DATA.BREW.BREAKS.length;
				for (i=0; i<breaks; i++) {
					$("#breakRow" + (i+1).toString()).show();
					$("#breakTemp" + (i+1).toString()).val(json.DATA.BREW.BREAKS[i].TEMP);
					$("#breakTime" + (i+1).toString()).val(json.DATA.BREW.BREAKS[i].TIME);
					$("#breakStatus" + (i+1).toString()).html(json.DATA.BREW.BREAKS[i].STATE);
				}
			}
			doPhases(json.DATA.BREW.MODE);
			if (setNext) {
				timer = setTimeout(function() {
					updateStatus(setNext);
				}, 1000);
			}
		}
	});
}

function myJSON(url, callback) {
	clearTimeout(timer);
	$.ajax({
		url: url,
		timeout: 10000,
	}).done(function(json) {
		$("#error").fadeOut();
		if (url != '/api/status') {
			updateStatus(true);
		}
		if (callback) {
			callback(json);
		}
	}).fail(function() {
		playSound("errorSound");
		$("#error").fadeIn(1000);
	});
}

function addBreakRow(id) {
	html = '<tr id="breakRowID"><td scope="row">ID</td><td><input type="number" id="breakTimeID" value="0" min="0" max="180" /></td><td><input type="number" id="breakTempID" value="0" min="0" max="100" /></td><td id="breakStatusID"></td></tr>';
	$("#breakBody").append(html.replace(/ID/g, id.toString()));
}

function doBreaksButtons() {
	for (i=1; i<=MAX_BREAKS; i++) {
		addBreakRow(i);
		$("#breakTemp" + i.toString()).prop("disabled", true);
		$("#breakTime" + i.toString()).prop("disabled", true);
	}

	for (i=breaks+1; i<=MAX_BREAKS; ++i) {
		$("#breakRow" + i.toString()).hide();
	}

	$("#startBrew").click(function() {
		myJSON('/api/brew?action=start');
	});

	$("#stopBrew").click(function() {
		myJSON('/api/brew?action=stop');
	});

	$("#editBreaks").click(function() {
		$("#editBreaks").attr("disabled", true);
		$("#saveBreaks").attr("disabled", false);
		$("#addBreakButton").attr("disabled", false);
		$("#removeBreakButton").attr("disabled", false);
		$("#startBrew").attr("disabled", true);
		for (i=1; i<=MAX_BREAKS; ++i) {
			$("#breakTemp" + i.toString()).prop("disabled", false);
			$("#breakTime" + i.toString()).prop("disabled", false);
		}
	});

	$("#saveBreaks").click(function() {
		$("#editBreaks").attr("disabled", false);
		$("#saveBreaks").attr("disabled", true);
		$("#addBreakButton").attr("disabled", true);
		$("#removeBreakButton").attr("disabled", true);
		$("#startBrew").attr("disabled", false);
		for (i=1; i<=MAX_BREAKS; ++i) {
			$("#breakTemp" + i.toString()).prop("disabled", true);
			$("#breakTime" + i.toString()).prop("disabled", true);
		}
		b = [];
		for (i=1; i<=breaks; ++i)
		{
			b.push({'temp' : parseInt($("#breakTemp" + i).val()), 'time' : parseInt($("#breakTime" + i).val())});
		}
		myJSON("/api/brew?breaks=" + JSON.stringify(b))
	});

	$("#addBreakButton").click(function() {
		$("#removeBreakButton").attr("disabled", false);
		breaks = Math.min(breaks + 1, MAX_BREAKS);
		if (breaks >= MAX_BREAKS) {
			$("#addBreakButton").attr("disabled", true);
		}
		$("#breakRow" + breaks.toString()).fadeIn('fast');
	});

	$("#removeBreakButton").click(function() {
		$("#addBreakButton").attr("disabled", false);
		$("#breakRow" + breaks.toString()).fadeOut('fast');
		breaks = Math.max(breaks - 1, 0);
		if (breaks <= 0) {
			$("#removeBreakButton").attr("disabled", true);
		}
	});
}

function doSlider() {
	$("#expectedTemperatureInput").slider();
	$("#expectedTemperatureInput").on("slide", function(evt) {
		$("#expectedTemperatureValue").text(evt.value);
	});
	$("#expectedTemperatureInput").on("slideStop", function(evt) {
		myJSON('/api/brew?temp=' + evt.value);
	});

	$("#pumpInput").slider();
	$("#pumpInput").on("slide", function(slideEvt) {
		$("#pumpValue").text(slideEvt.value);
	});
	$("#pumpInput").on("slideStop", function(evt) {
		myJSON('/api/pump?level=' + evt.value);
	});

	$("#fanInput").slider();
	$("#fanInput").on("slide", function(slideEvt) {
		$("#fanValue").text(slideEvt.value);
	});
	$("#fanInput").on("slideStop", function(evt) {
		myJSON('/api/fan?level=' + evt.value);
	});
}

function playSound(id) {
	if ($('#soundCheckbox').is(':checked')) {
		document.getElementById(id).play();
	}
}

function formatSeconds(totalSeconds) {
	days = Math.floor(totalSeconds / 86400);
	hours   = Math.floor(totalSeconds % 86400 / 3600);
	minutes = Math.floor(totalSeconds % 3600 / 60);
	seconds = Math.floor(totalSeconds % 60);
	str = [hours, minutes, seconds].map(function(t) { return t >= 10 ? t : '0' + t; }).join(':');
	if (days > 0) {
		return days + 'd ' + str;
	}
	else {
		return str;
	}
}
