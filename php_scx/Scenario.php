<?php
    function Scenario(){

        Trig('Init');
        SetPlayersCount(2);
        SetMapSize(34);
        SetAllTech(True);

        foreach([1,2] as $p) {
            SetPlayerCiv($p, 'Chinese');
            SetPlayerStartAge($p, 'Castle');
        }

        
SetPlayerName(1, "Artillery");
SetPlayerName(2, "bot3");
        
NewObject(1, 46, [10, 10], 0);
NewObject(1, 38, [10, 10], 0);
Efft_Research(1, 211);
Efft_Research(1, 39);
NewObject(1, 279, [10, 10], 0);
NewObject(1, 279, [10, 10], 0);
NewObject(1, 279, [10, 10], 0);
NewObject(1, 725, [10, 10], 0);
NewObject(1, 775, [10, 10], 0);
NewObject(1, 282, [10, 10], 0);
NewObject(1, 771, [10, 10], 0);
NewObject(1, 35, [10, 10], 0);
Efft_Research(1, 67);
Efft_Research(1, 81);
NewObject(1, 6, [10, 10], 0);
NewObject(1, 827, [10, 10], 0);
NewObject(1, 827, [10, 10], 0);
Efft_Research(1, 437);
NewObject(1, 873, [10, 10], 0);
NewObject(1, 11, [10, 10], 0);
NewObject(1, 753, [10, 10], 0);
NewObject(1, 8, [10, 10], 0);
NewObject(1, 8, [10, 10], 0);
NewObject(1, 8, [10, 10], 0);
NewObject(1, 866, [10, 10], 0);
NewObject(1, 358, [10, 10], 0);
NewObject(1, 358, [10, 10], 0);
Efft_Research(1, 199);
NewObject(1, 24, [10, 10], 0);
NewObject(1, 280, [10, 10], 0);
NewObject(1, 77, [10, 10], 0);
NewObject(1, 73, [10, 10], 0);
NewObject(1, 583, [10, 10], 0);
NewObject(1, 583, [10, 10], 0);
Efft_Research(1, 74);
NewObject(1, 876, [10, 10], 0);
NewObject(1, 876, [10, 10], 0);
NewObject(1, 39, [10, 10], 0);
NewObject(1, 882, [10, 10], 0);
NewObject(1, 125, [10, 10], 0);
NewObject(1, 281, [10, 10], 0);
NewObject(1, 185, [10, 10], 0);
NewObject(1, 692, [10, 10], 0);
NewObject(1, 291, [10, 10], 0);
NewObject(2, 46, [24, 24], 0);
NewObject(2, 25, [24, 24], 0);
Efft_Research(2, 211);
Efft_Research(2, 39);
NewObject(2, 279, [24, 24], 0);
NewObject(2, 775, [24, 24], 0);
NewObject(2, 282, [24, 24], 0);
NewObject(2, 282, [24, 24], 0);
NewObject(2, 771, [24, 24], 0);
NewObject(2, 35, [24, 24], 0);
NewObject(2, 755, [24, 24], 0);
Efft_Research(2, 67);
Efft_Research(2, 81);
NewObject(2, 329, [24, 24], 0);
NewObject(2, 6, [24, 24], 0);
NewObject(2, 763, [24, 24], 0);
NewObject(2, 827, [24, 24], 0);
NewObject(2, 827, [24, 24], 0);
NewObject(2, 239, [24, 24], 0);
Efft_Research(2, 437);
NewObject(2, 41, [24, 24], 0);
NewObject(2, 879, [24, 24], 0);
NewObject(2, 11, [24, 24], 0);
NewObject(2, 11, [24, 24], 0);
NewObject(2, 753, [24, 24], 0);
NewObject(2, 753, [24, 24], 0);
NewObject(2, 8, [24, 24], 0);
NewObject(2, 232, [24, 24], 0);
NewObject(2, 358, [24, 24], 0);
Efft_Research(2, 199);
NewObject(2, 24, [24, 24], 0);
NewObject(2, 280, [24, 24], 0);
NewObject(2, 77, [24, 24], 0);
NewObject(2, 73, [24, 24], 0);
Efft_Research(2, 74);
NewObject(2, 39, [24, 24], 0);
NewObject(2, 125, [24, 24], 0);
NewObject(2, 125, [24, 24], 0);
NewObject(2, 281, [24, 24], 0);
NewObject(2, 185, [24, 24], 0);
NewObject(2, 291, [24, 24], 0);
NewObject(2, 869, [24, 24], 0);

        Trig("Start");
        Cond_Timer(1);
        Efft_Give(1, 50000, STONE);  # Needed for consistent screenshot recognition
        
Efft_PatrolO(1, Area(6, 6, 14, 14), [24, 24]);
Efft_PatrolO(2, Area(20, 20, 28, 28), [10, 10]);
Efft_ChangeView(1, [16,17]);
Efft_Chat(1, "3 Scorpion - 3 Longbowman - 2 War Wagon - 2 Pikeman");
Efft_Chat(1, "2 Genitour - 2 Boyar - 1 Janissary - 1 Knight");
Efft_Chat(1, "1 Padded Archer Armor - 1 Jaguar Warrior - 1 Missionary - 1 Mameluke");
Efft_Chat(1, "1 Conquistador - 1 Battering Ram - 1 Forging - 1 Elite Skirmisher");
Efft_Chat(1, "1 Elephant Archer - 1 Mangudai - 1 Eagle Warrior - 1 Genoese Crossbowman");
Efft_Chat(1, "1 Fletching - 1 Crossbow - 1 Mangonel - 1 Long Sword");
Efft_Chat(1, "1 Chu Ko Nu - 1 Scale Mail - 1 Cavalry Archer - 1 Condottierro");
Efft_Chat(1, "1 Monk - 1 Throwing Axeman - 1 Slinger - 1 Berserk");
Efft_Chat(1, "1 Samurai");
Efft_Chat(2, "2 Mameluke - 2 War Wagon - 2 Mangudai - 2 Eagle Warrior");
Efft_Chat(2, "2 Monk - 1 Janissary - 1 Teutonic Knight - 1 Husbandry");
Efft_Chat(2, "1 Scorpion - 1 Missionary - 1 Conquistador - 1 Battering Ram");
Efft_Chat(2, "1 Tarkan - 1 Camel - 1 Elite Skirmisher - 1 Plumed Archer");
Efft_Chat(2, "1 War Elephant - 1 Huskarl - 1 Kamayuk - 1 Longbowman");
Efft_Chat(2, "1 Woad Raider - 1 Pikeman - 1 Fletching - 1 Crossbow");
Efft_Chat(2, "1 Mangonel - 1 Long Sword - 1 Chu Ko Nu - 1 Scale Mail");
Efft_Chat(2, "1 Cavalry Archer - 1 Throwing Axeman - 1 Slinger - 1 Samurai");
Efft_Chat(2, "1 Magyar Huszar");
    }
?>