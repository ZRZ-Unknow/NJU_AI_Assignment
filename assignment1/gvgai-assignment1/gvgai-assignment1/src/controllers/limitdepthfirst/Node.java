package controllers.limitdepthfirst;

import core.game.Observation;
import core.game.StateObservation;
import ontology.Types;
import tools.Vector2d;
import java.util.ArrayList;

public class Node implements Comparable<Node>{
    public Node parent;
    public StateObservation state;
    public int depth;
    public double H;
    public Node root_node;
    public Node(StateObservation state, int depth){
        this.state = state.copy();
        this.depth = depth;
        heuristic();
    }
    public void heuristic() {
        if (this.state.getGameWinner()== Types.WINNER.PLAYER_WINS){
            this.H= Double.NEGATIVE_INFINITY;
        }
        else {
            ArrayList[] fixedPositions = state.getImmovablePositions();
            ArrayList[] movingPositions = state.getMovablePositions();
            Vector2d goal_pos = ((Observation)(fixedPositions[1]).get(0)).position;
            Vector2d key_pos = ((Observation)(movingPositions[0].get(0))).position;
            Vector2d avatar_pos = state.getAvatarPosition();
            if (state.getAvatarType()==1){
                this.H=avatar_pos.dist(key_pos)+key_pos.dist(goal_pos);
            }
            else{
                this.H=avatar_pos.dist(goal_pos);
            }
        }
    }
    @Override
    public int compareTo(Node n){
        return (int) (this.H-n.H);
    }
}
