<?php
    function Scenario(){

        Trig('Init');
        SetPlayersCount(2);
        SetMapSize(34);
        SetAllTech(True);

        foreach([1,2] as $$p) {
            SetPlayerCiv($$p, 'Chinese');
            SetPlayerStartAge($$p, 'Castle');
        }

        $SetPlayerNames
        $AddUnitsTechs

        Trig("Start");
        Cond_Timer(1);
        Efft_Give(1, 50000, STONE);  # Needed for consistent screenshot recognition
        $InitialActions
    }
?>