<?php

function Scenario(){

    # For example we will make a tiny 8 players map:
    SetPlayersCount(8);
    SetMapSize(50);

    # Send a message at 10 seconds to all players
	Trig('Send a message to all players',1,0);
	Cond_Timer(10);
	foreach(range(1,8) as $p){
	   Efft_Chat($p,'Hello World');
    }

    # Kill all military units of player 2 at 20 seconds
	Trig('Kill player 2 military units',1,0);
	Cond_Timer(20);
	Efft_KillY(2,Y_MILITARY);

    # Kill all military units of all players at middle zone 16x16 of the map at 20 seconds
    $mapSize = GetMapSize();
	Trig('Kill all players military units at middle',1,0);
	Cond_Timer(20);
    $X1 = $Y1 = $mapSize/2 - 8;
    $X2 = $Y2 = $mapSize/2 + 8;
	foreach(range(1,8) as $player){
	   Efft_KillY($player,Y_MILITARY,Area($X1,$Y1,$X2,$Y2));
	}
    # With explosions effect
    for($y = $Y1; $y < $Y2; $y++)
        for($x = $X1; $x < $X2; $x++)
            Efft_Create(0,U_MACAW,array($x,$y));
    Efft_KillU(0,U_MACAW,Area($X1,$Y1,$X2,$Y2));

    # Activate "Send a message to all players" again at 30 seconds
	Trig('Reactivate Send a message to all players',1,0);
	Cond_Timer(30);
	Efft_Act('Send a message to all players');

    # Put dirt 1 everywhere (to make terrain from image use SetTerrainFromImage())
    $mapSize = GetMapSize();
    for($y = 0; $y < $mapSize; $y++)
       for($x = 0; $x < $mapSize; $x++)
           SetTerrainCell($x,$y,array('terrain' => TERRAIN_DIRT_1));

    # Add 100 militia to all players randomly everywhere on the map
    $mapSize = GetMapSize();
    foreach(range(1,8) as $player){
        for($i = 0; $i < 100; $i++){
            $x = rand(0,$mapSize - 1);
            $y = rand(0,$mapSize - 1);
            $r = rand(0,360);
            NewObject($player,U_MILITIA,array($x,$y),$r);
	   }
    }

    # Write instructions
    SetMessageObjective('Hello World');

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



