package controllers.Astar;
import core.game.Observation;
import core.game.StateObservation;
import ontology.Types;
import tools.Vector2d;

import java.util.ArrayList;

public class Node implements Comparable<Node>{
    public double H;
    public double G;
    public double F;
    public Node parent;
    public StateObservation state;

    public Node(StateObservation stateObs){
        this.state = stateObs.copy();
    }

    public void upDate(){
        this.G=this.parent.G+1;
        heuristic();
        this.F=this.G+this.H;
    }

    public int compareTo(Node node){
        return (int)(this.F-node.F);
    }

    public void heuristic() {
        if (this.state.getGameWinner()== Types.WINNER.PLAYER_WINS){
            this.H=Double.NEGATIVE_INFINITY;
        }
        else if (this.state.getGameWinner()== Types.WINNER.PLAYER_LOSES){
            this.H=Double.POSITIVE_INFINITY;
        }
        else {
            double K = -10,k=100;
            double box_bias=0,hole_bias=0;
            ArrayList[] fixedPositions = this.state.getImmovablePositions();
            ArrayList[] movingPositions = this.state.getMovablePositions();
            if(fixedPositions.length == 5){
                ArrayList<Observation> hole = fixedPositions[1];
                ArrayList<Observation> box = movingPositions[1];
                for(int i=0;i<box.size();i++){
                    box_bias+=1;
                }
                for(int i=0;i<hole.size();i++){
                    hole_bias+=1;
                }
            }
            Vector2d goal_pos = ((Observation)(fixedPositions[0]).get(0)).position;
            Vector2d avatar_pos = state.getAvatarPosition();
            if (this.state.getAvatarType() == 1) {
                Vector2d key_pos = ((Observation)(movingPositions[0].get(0))).position;
                this.H=K*this.state.getGameScore()+ key_pos.dist(avatar_pos) + goal_pos.dist(key_pos)+k*hole_bias+k*box_bias;
            }
            else {
                this.H=K*this.state.getGameScore() + goal_pos.dist(avatar_pos)+k*hole_bias+k*box_bias;
            }
        }
    }
}
