package controllers.Astar;

import core.game.StateObservation;
import core.player.AbstractPlayer;
import ontology.Types;
import tools.ElapsedCpuTimer;
import java.util.ArrayList;
import java.util.PriorityQueue;

public class Agent extends AbstractPlayer {
    private ArrayList<StateObservation> closedList = new ArrayList<>();
    private PriorityQueue<Node> openList = new PriorityQueue<>();
    private ArrayList<Types.ACTIONS> executable_action = new ArrayList<>();
    private Node bestNode;

    public void init() {
        bestNode=null;
        openList.clear();
        closedList.clear();
        executable_action.clear();
    }

    public boolean isInClosedList(StateObservation obs) {
        for (StateObservation so : closedList) {
            if (so.equalPosition(obs)) {
                return true;
            }
        }
        return false;
    }

    public boolean isInOpenList(StateObservation obs) {
        for (Node node : openList) {
            if (node.state.equalPosition(obs)) {
                return true;
            }
        }
        return false;
    }

    public Agent(StateObservation so, ElapsedCpuTimer elapsedTimer) {
        init();
        astarSearch(so);
    }

    public void astarSearch(StateObservation stateObs) {
        Node root_node = new Node(stateObs);
        root_node.parent=null;
        root_node.G=0;
        openList.add(root_node);

        while (!openList.isEmpty()) {
            Node curr_node = openList.poll();
            if(!curr_node.state.isGameOver())
            {bestNode=curr_node;}
            executable_action = curr_node.state.getAvailableActions();
            closedList.add(curr_node.state.copy());

            for (Types.ACTIONS action : executable_action) {
                StateObservation stCopy = curr_node.state.copy();
                stCopy.advance(action);

                if (stCopy.isGameOver()){
                    if (stCopy.getGameWinner() == Types.WINNER.PLAYER_WINS) {
                        Node newNode=new Node(stCopy);
                        newNode.parent=curr_node;
                        newNode.upDate();
                        bestNode=newNode;
                        return;
                    }
                    else{
                        continue;
                    }
                }
                else if (isInClosedList(stCopy)) {
                    continue;
                }
                else if (isInOpenList(stCopy)) {
                    for (Node node : openList) {
                        if (node.state.equalPosition(stCopy)) {
                            if (node.G>curr_node.G+1) {
                                openList.remove(node);
                                Node newNode=new Node(stCopy);
                                newNode.parent=curr_node;
                                newNode.upDate();
                                openList.add(newNode);
                                break;
                            }
                        }
                    }
                }
                else {
                    Node newNode=new Node(stCopy);
                    newNode.parent=curr_node;
                    newNode.upDate();
                    openList.add(newNode);
                }

            }
        }
    }

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        Types.ACTIONS action = null;
        if(bestNode==null){
            astarSearch(stateObs);
            return null;
        }
        Node p=bestNode;
        Node q=p;
        int i=0;
        while(p!= null && p.parent != null && p.parent.parent != null){
            p = p.parent;
            if (i>0){q=q.parent;}
            i++;
        }
        if(p != null && q!=null)
            action=p.state.getAvatarLastAction();
            q.parent=p.parent;
            return action;

    }
}