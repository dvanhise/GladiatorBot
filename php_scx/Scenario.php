<?php

function Scenario(){
    SetPlayersCount(2);
    SetMapSize(50);

    /*SetPlayersCount(2);
    SetMapSize(50);

    $homeCompFile = fopen('./home.yaml', 'r');
    $awayCompFile = fopen('./away.yaml', 'r');

    $homeComp = yaml_parse(fread($homeCompFile));
    $awayComp = yaml_parse(fread($awayCompFile));

    foreach($homeComp as $name => $count) {
        if (substr($name, 0, 1 ) === "U") {
            NewObject(1, eval($name), [20, 30], 0);
        } else {
            Efft_Research(1, eval($name));
        }
    }

    foreach($awayComp as $name => $count) {
        if (substr($name, 0, 1 ) === "U") {
            NewObject(2, eval($name), [30, 20], 0);
        } else {
            Efft_Research(2, eval($name));
        }
    }*/
}

?>



