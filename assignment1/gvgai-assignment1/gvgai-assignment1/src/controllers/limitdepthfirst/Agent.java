package controllers.limitdepthfirst;

import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.Stack;
import core.player.AbstractPlayer;
import core.game.StateObservation;
import ontology.Types;
import tools.ElapsedCpuTimer;

public class Agent extends AbstractPlayer {

    private final int max_depth=4;
    private Stack<Node> node_stack = new Stack<Node>();
    private ArrayList<StateObservation> acted_state = new ArrayList<StateObservation>();
    private PriorityQueue<Node> node_queue = new PriorityQueue<Node>();
    private ArrayList<Types.ACTIONS> executable_action = new ArrayList<Types.ACTIONS>();

    public Agent (StateObservation so, ElapsedCpuTimer elapsedTimer) {}

    private void clear(){
        node_stack.clear();
        node_queue.clear();
        acted_state.clear();
        executable_action.clear();
    }

    private void init(StateObservation stateObs){
        Node node = new Node(stateObs, 0);
        node.parent = null;
        node.root_node=null;
        node_stack.push(node);
        executable_action=stateObs.getAvailableActions();
    }

    private boolean isInActedState(StateObservation stateObs){
        for(StateObservation so:acted_state){
            if(so.equalPosition(stateObs)){
                return true;
            }
        }
        return false;
    }

    public Types.ACTIONS LDFS() {
        while (!node_stack.isEmpty()) {
            Node curr_node = node_stack.pop();
            StateObservation curr_state = curr_node.state.copy();
            int curr_depth = curr_node.depth;

            if (curr_state.isGameOver()) {
                if (curr_state.getGameWinner() == Types.WINNER.PLAYER_WINS) {
                    node_queue.add(curr_node);
                    break;
                }
                else{
                    acted_state.add(curr_state);
                    continue;
                }
            }

            acted_state.add(curr_state);
            if (curr_depth < max_depth) {
                for (Types.ACTIONS action : executable_action) {
                    StateObservation stCopy = curr_state.copy();
                    stCopy.advance(action);
                    if (!isInActedState(stCopy) ){
                        Node node = new Node(stCopy, curr_depth + 1);
                        node.parent = curr_node;
                        if (curr_node.root_node==null) {
                            node.root_node =node;
                        }
                        else{
                            node.root_node=curr_node.root_node;
                        }
                        node_stack.push(node);
                        }
                    }
                }
            else {
                node_queue.add(curr_node);
            }
        }
        Node node=node_queue.peek();
        Types.ACTIONS action=node.root_node.state.getAvatarLastAction();
        return action;
    }

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        Types.ACTIONS action = null;
        init(stateObs);
        action=LDFS();
        clear();
        return action;
    }
}
