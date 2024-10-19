#ifndef PLAYER_H
#define PLAYER_H

#include "sgd/sgd.h"
#include "misc_functions.h"

// Player animation sequences
const int ANIM_DANCING = 0;
const int ANIM_FALLING = 1;
const int ANIM_IDLE = 2;
const int ANIM_JUMPING = 3;
const int ANIM_RUNNING = 4;
const int ANIM_SLIDING = 5;

class Player {
public:
    Player();
	void Update();
	void GenshinInput();	
    void Dance();
    void Run();
    bool dancing, falling, idle, jumping, running, sliding, gamepad;    
	SGD_Model pivot;
	void ReportStats();
private:    
    SGD_Model view_model;
    SGD_Model collision_model;
    SGD_Collider collider;
    Utils::Vec3 acceleration;
    Utils::Vec3 velocity;    
    int nseq, seq0, seq1;
    float time0, time0Step, time1, time1Step, blend, blendStep, animation_speed;
	void ProcessAnimation();	
    void Move();
	void HandleCollision();	
};

#endif // PLAYER_H
