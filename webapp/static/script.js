
// Javascript is insane.

const country_codes = {
  "AF": "Afghanistan",
  "AX": "Aland Islands",
  "AL": "Albania",
  "DZ": "Algeria",
  "AS": "American Samoa",
  "AD": "Andorra",
  "AO": "Angola",
  "AI": "Anguilla",
  "AQ": "Antarctica",
  "AG": "Antigua And Barbuda",
  "AR": "Argentina",
  "AM": "Armenia",
  "AW": "Aruba",
  "AU": "Australia",
  "AT": "Austria",
  "AZ": "Azerbaijan",
  "BS": "Bahamas",
  "BH": "Bahrain",
  "BD": "Bangladesh",
  "BB": "Barbados",
  "BY": "Belarus",
  "BE": "Belgium",
  "BZ": "Belize",
  "BJ": "Benin",
  "BM": "Bermuda",
  "BT": "Bhutan",
  "BO": "Bolivia",
  "BA": "Bosnia And Herzegovina",
  "BW": "Botswana",
  "BV": "Bouvet Island",
  "BR": "Brazil",
  "IO": "British Indian Ocean Territory",
  "BN": "Brunei Darussalam",
  "BG": "Bulgaria",
  "BF": "Burkina Faso",
  "BI": "Burundi",
  "KH": "Cambodia",
  "CM": "Cameroon",
  "CA": "Canada",
  "CV": "Cape Verde",
  "KY": "Cayman Islands",
  "CF": "Central African Republic",
  "TD": "Chad",
  "CL": "Chile",
  "CN": "China",
  "CX": "Christmas Island",
  "CC": "Cocos (Keeling) Islands",
  "CO": "Colombia",
  "KM": "Comoros",
  "CG": "Congo",
  "CD": "Congo, Democratic Republic",
  "CK": "Cook Islands",
  "CR": "Costa Rica",
  "CI": "Cote D\"Ivoire",
  "HR": "Croatia",
  "CU": "Cuba",
  "CY": "Cyprus",
  "CZ": "Czech Republic",
  "DK": "Denmark",
  "DJ": "Djibouti",
  "DM": "Dominica",
  "DO": "Dominican Republic",
  "EC": "Ecuador",
  "EG": "Egypt",
  "SV": "El Salvador",
  "GQ": "Equatorial Guinea",
  "ER": "Eritrea",
  "EE": "Estonia",
  "ET": "Ethiopia",
  "FK": "Falkland Islands (Malvinas)",
  "FO": "Faroe Islands",
  "FJ": "Fiji",
  "FI": "Finland",
  "FR": "France",
  "GF": "French Guiana",
  "PF": "French Polynesia",
  "TF": "French Southern Territories",
  "GA": "Gabon",
  "GM": "Gambia",
  "GE": "Georgia",
  "DE": "Germany",
  "GH": "Ghana",
  "GI": "Gibraltar",
  "GR": "Greece",
  "GL": "Greenland",
  "GD": "Grenada",
  "GP": "Guadeloupe",
  "GU": "Guam",
  "GT": "Guatemala",
  "GG": "Guernsey",
  "GN": "Guinea",
  "GW": "Guinea-Bissau",
  "GY": "Guyana",
  "HT": "Haiti",
  "HM": "Heard Island & Mcdonald Islands",
  "VA": "Holy See (Vatican City State)",
  "HN": "Honduras",
  "HK": "Hong Kong",
  "HU": "Hungary",
  "IS": "Iceland",
  "IN": "India",
  "ID": "Indonesia",
  "IR": "Iran, Islamic Republic Of",
  "IQ": "Iraq",
  "IE": "Ireland",
  "IM": "Isle Of Man",
  "IL": "Israel",
  "IT": "Italy",
  "JM": "Jamaica",
  "JP": "Japan",
  "JE": "Jersey",
  "JO": "Jordan",
  "KZ": "Kazakhstan",
  "KE": "Kenya",
  "KI": "Kiribati",
  "KR": "Korea",
  "KP": "North Korea",
  "KW": "Kuwait",
  "KG": "Kyrgyzstan",
  "LA": "Lao People\"s Democratic Republic",
  "LV": "Latvia",
  "LB": "Lebanon",
  "LS": "Lesotho",
  "LR": "Liberia",
  "LY": "Libyan Arab Jamahiriya",
  "LI": "Liechtenstein",
  "LT": "Lithuania",
  "LU": "Luxembourg",
  "MO": "Macao",
  "MK": "Macedonia",
  "MG": "Madagascar",
  "MW": "Malawi",
  "MY": "Malaysia",
  "MV": "Maldives",
  "ML": "Mali",
  "MT": "Malta",
  "MH": "Marshall Islands",
  "MQ": "Martinique",
  "MR": "Mauritania",
  "MU": "Mauritius",
  "YT": "Mayotte",
  "MX": "Mexico",
  "FM": "Micronesia, Federated States Of",
  "MD": "Moldova",
  "MC": "Monaco",
  "MN": "Mongolia",
  "ME": "Montenegro",
  "MS": "Montserrat",
  "MA": "Morocco",
  "MZ": "Mozambique",
  "MM": "Myanmar",
  "NA": "Namibia",
  "NR": "Nauru",
  "NP": "Nepal",
  "NL": "Netherlands",
  "AN": "Netherlands Antilles",
  "NC": "New Caledonia",
  "NZ": "New Zealand",
  "NI": "Nicaragua",
  "NE": "Niger",
  "NG": "Nigeria",
  "NU": "Niue",
  "NF": "Norfolk Island",
  "MP": "Northern Mariana Islands",
  "NO": "Norway",
  "OM": "Oman",
  "PK": "Pakistan",
  "PW": "Palau",
  "PS": "Palestinian Territory, Occupied",
  "PA": "Panama",
  "PG": "Papua New Guinea",
  "PY": "Paraguay",
  "PE": "Peru",
  "PH": "Philippines",
  "PN": "Pitcairn",
  "PL": "Poland",
  "PT": "Portugal",
  "PR": "Puerto Rico",
  "QA": "Qatar",
  "RE": "Reunion",
  "RO": "Romania",
  "RU": "Russian Federation",
  "RW": "Rwanda",
  "BL": "Saint Barthelemy",
  "SH": "Saint Helena",
  "KN": "Saint Kitts And Nevis",
  "LC": "Saint Lucia",
  "MF": "Saint Martin",
  "PM": "Saint Pierre And Miquelon",
  "VC": "Saint Vincent And Grenadines",
  "WS": "Samoa",
  "SM": "San Marino",
  "ST": "Sao Tome And Principe",
  "SA": "Saudi Arabia",
  "SN": "Senegal",
  "RS": "Serbia",
  "SC": "Seychelles",
  "SL": "Sierra Leone",
  "SG": "Singapore",
  "SK": "Slovakia",
  "SI": "Slovenia",
  "SB": "Solomon Islands",
  "SO": "Somalia",
  "ZA": "South Africa",
  "GS": "South Georgia And Sandwich Isl.",
  "ES": "Spain",
  "LK": "Sri Lanka",
  "SD": "Sudan",
  "SR": "Suriname",
  "SJ": "Svalbard And Jan Mayen",
  "SZ": "Swaziland",
  "SE": "Sweden",
  "CH": "Switzerland",
  "SY": "Syrian Arab Republic",
  "TW": "Taiwan",
  "TJ": "Tajikistan",
  "TZ": "Tanzania",
  "TH": "Thailand",
  "TL": "Timor-Leste",
  "TG": "Togo",
  "TK": "Tokelau",
  "TO": "Tonga",
  "TT": "Trinidad And Tobago",
  "TN": "Tunisia",
  "TR": "Turkey",
  "TM": "Turkmenistan",
  "TC": "Turks And Caicos Islands",
  "TV": "Tuvalu",
  "UG": "Uganda",
  "UA": "Ukraine",
  "AE": "United Arab Emirates",
  "GB": "United Kingdom",
  "US": "United States",
  "UM": "United States Outlying Islands",
  "UY": "Uruguay",
  "UZ": "Uzbekistan",
  "VU": "Vanuatu",
  "VE": "Venezuela",
  "VN": "Vietnam",
  "VG": "Virgin Islands, British",
  "VI": "Virgin Islands, U.S.",
  "WF": "Wallis And Futuna",
  "EH": "Western Sahara",
  "YE": "Yemen",
  "ZM": "Zambia",
  "ZW": "Zimbabwe"
}

var entries = [
  {
    "timestamp": 1622745056,
    "username": "postgres",
    "nation": "in"
  },
  {
    "timestamp": 1622745054,
    "username": "gabriel",
    "nation": "it"
  },
  {
    "timestamp": 1622745050,
    "username": "root",
    "nation": "cn"
  },
  {
    "timestamp": 1622745048,
    "username": "music",
    "nation": "cn"
  },
  {
    "timestamp": 1622745042,
    "username": "admin1",
    "nation": "fr"
  },
  {
    "timestamp": 1622744983,
    "username": "test7",
    "nation": "kr"
  },
  {
    "timestamp": 1622744973,
    "username": "delta",
    "nation": "ca"
  },
  {
    "timestamp": 1622744942,
    "username": "livio2",
    "nation": "in"
  },
  {
    "timestamp": 1622744934,
    "username": "zchu",
    "nation": "us"
  },
  {
    "timestamp": 1622744932,
    "username": "gmod",
    "nation": "cn"
  },
  {
    "timestamp": 1622744924,
    "username": "jack",
    "nation": "it"
  },
  {
    "timestamp": 1622744909,
    "username": "meng",
    "nation": "cn"
  },
  {
    "timestamp": 1622744857,
    "username": "elk",
    "nation": "fr"
  },
  {
    "timestamp": 1622744853,
    "username": "git",
    "nation": "kr"
  },
  {
    "timestamp": 1622744834,
    "username": "node1",
    "nation": "ca"
  },
  {
    "timestamp": 1622744824,
    "username": "ubuntu",
    "nation": "in"
  },
  {
    "timestamp": 1622744815,
    "username": "root",
    "nation": "ca"
  },
  {
    "timestamp": 1622744815,
    "username": "es",
    "nation": "cn"
  },
  {
    "timestamp": 1622744814,
    "username": "root",
    "nation": "ca"
  },
  {
    "timestamp": 1622744811,
    "username": "kafka",
    "nation": "in"
  },
  {
    "timestamp": 1622744796,
    "username": "test5",
    "nation": "it"
  },
  {
    "timestamp": 1622744788,
    "username": "user",
    "nation": "us"
  },
  {
    "timestamp": 1622744774,
    "username": "user3",
    "nation": "cn"
  },
  {
    "timestamp": 1622744739,
    "username": "guest",
    "nation": "us"
  },
  {
    "timestamp": 1622744721,
    "username": "server",
    "nation": "kr"
  },
  {
    "timestamp": 1622744705,
    "username": "git",
    "nation": "in"
  },
  {
    "timestamp": 1622744698,
    "username": "limy",
    "nation": "ca"
  },
  {
    "timestamp": 1622744693,
    "username": "google",
    "nation": "cn"
  },
  {
    "timestamp": 1622744667,
    "username": "luanmingfu",
    "nation": "it"
  },
  {
    "timestamp": 1622744642,
    "username": "root",
    "nation": "us"
  },
  {
    "timestamp": 1622744638,
    "username": "sinusbot",
    "nation": "cn"
  },
  {
    "timestamp": 1622744638,
    "username": "user2",
    "nation": "us"
  },
  {
    "timestamp": 1622744592,
    "username": "gaoguangyuan",
    "nation": "in"
  },
  {
    "timestamp": 1622744589,
    "username": "sinus",
    "nation": "kr"
  },
  {
    "timestamp": 1622744572,
    "username": "backup",
    "nation": "cn"
  },
  {
    "timestamp": 1622744563,
    "username": "megan",
    "nation": "ca"
  },
  {
    "timestamp": 1622744550,
    "username": "qwang",
    "nation": "us"
  },
  {
    "timestamp": 1622744543,
    "username": "support",
    "nation": "it"
  },
  {
    "timestamp": 1622744498,
    "username": "elasticsearch",
    "nation": "cn"
  },
  {
    "timestamp": 1622744491,
    "username": "test",
    "nation": "us"
  },
  {
    "timestamp": 1622744489,
    "username": "matt",
    "nation": "fr"
  },
  {
    "timestamp": 1622744473,
    "username": "csserver",
    "nation": "in"
  },
  {
    "timestamp": 1622744464,
    "username": "doudou",
    "nation": "kr"
  },
  {
    "timestamp": 1622744458,
    "username": "bob",
    "nation": "us"
  },
  {
    "timestamp": 1622744434,
    "username": "es",
    "nation": "ca"
  },
  {
    "timestamp": 1622744430,
    "username": "mediafire",
    "nation": "cn"
  },
  {
    "timestamp": 1622744419,
    "username": "e",
    "nation": "it"
  },
  {
    "timestamp": 1622744362,
    "username": "azureuser",
    "nation": "us"
  },
  {
    "timestamp": 1622744360,
    "username": "administrator",
    "nation": "cn"
  },
  {
    "timestamp": 1622744350,
    "username": "2",
    "nation": "in"
  }
]

shuffle(entries)
//var s = recent_attack_str_update(strs, entries, 28)
//for (let step = 0; step < 5; step++) {
//    console.log(s)
//
//    s = recent_attack_str_update(s, entries, 28)
//}

document.addEventListener(
    'DOMContentLoaded',
    function() {
        //document.getElementById("recent_attacks").innerHTML = s.join("");

        update_recent_attacks_section(entries, 28);
    },
    false
);

console.log(Object.entries(country_codes))

// ============================================================================

// `prev_lines` is an array of strings, ostensibly this function's previous return.
// `new_entries` is an object with the raw entry data.
// Return an array of entry strings no longer than `max_lines`.
function recent_attack_str_update(prev_lines, new_entries, max_lines) {
    lines = []
    for (const entry of new_entries) {
        if (lines.length < max_lines) {
            lines.push(`<p>${entry.nation} -- ${entry.username}</p>`)
        } else break
    }

    for (const line of prev_lines) {
        if (lines.length < max_lines) {
            lines.push(line)
        } else break
    }
    return lines.reverse()
}

function update_recent_attacks_section(new_entries, max_lines) {
    line_count = document.getElementById("recent_attacks").innerHTML.split(/\r\n|\r|\n/).length;

    var offset = 0;
    for (const [i, entry] of new_entries.entries()) {
        timeout = i * 100;
        setTimeout(
            function() {
                document.getElementById("recent_attacks").innerHTML += `<p>${entry.nation} -- ${entry.username}</p>`;
            },
            timeout
        );
        if ((line_count + i - offset) > max_lines) {
            line_count = 0;
            offset += max_lines;
            setTimeout(
                function() {
                    document.getElementById("recent_attacks").innerHTML = "";
                },
                timeout
            );
        }
    }
}

async function nation_report_update(country_code) {
    result = await fetch("/api/ssh_attack_summary.json")
    .then(response => response.json())
    country_all_attacks = (result[country_code])
}

function shuffle(array) {
  var currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}


function blink_country(country) {
    country.classList.add("blink");
    setTimeout(
        function() { country.classList.remove("blink"); },
        6000
    );
}

// ============================================================================

window.addEventListener("load",
    function() {
        var previously_selected_country = null;

        var svgObject = document.getElementById('map_svg').contentDocument;
        var country = svgObject.getElementById('cn');
        blink_country(country);
        var country = svgObject.getElementById('ca');
        blink_country(country);

        svgObject.addEventListener(
            "mousedown", function(event)
            {
                if (event.which != 1) return;

                // Walk up to the first ID that's a two-letter country code.
                var e = event.target
                while (e != null) {
                    if (Object.keys(country_codes).includes(e.id.toUpperCase())) {
                        var country_code = e.id.toUpperCase()
                        var country_name = country_codes[country_code]
                        break
                    } else {
                        e = e.parentElement
                    }
                }

                if (country_code != undefined) {
                    if (previously_selected_country != null) {
                        previously_selected_country.classList.remove("selected")
                    }
                    document.getElementById("country_code_display").innerHTML = "<div>" + country_code + "</div>";
                    var country = svgObject.getElementById(country_code.toLowerCase());

                    // Blink country (SVG object) and country code display (HTML div).
                    country.classList.add("selected")
                    document.getElementById("country_code_display").firstChild.classList.add("quick_blink")

                    ///fetch('/api/ssh_attack_data.json?nation=' + country_code.toLowerCase())
                    ///.then(response => response.json())
                    ///.then(data => console.log(data));

                    nation_report_update(country_code.toLowerCase())
                    previously_selected_country = country;
                }
            },
            false
        );
    }
);
