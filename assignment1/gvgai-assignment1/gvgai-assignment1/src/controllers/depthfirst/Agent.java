package controllers.depthfirst;

import java.util.ArrayList;
import java.util.Stack;
import core.game.StateObservation;
import ontology.Types;
import core.player.AbstractPlayer;
import tools.ElapsedCpuTimer;

public class Agent extends AbstractPlayer {
    private Stack<StateObservation> state_stack = new Stack<StateObservation>();
    private ArrayList<Types.ACTIONS> action_list = new ArrayList<Types.ACTIONS>();
    private Stack<Types.ACTIONS> success_action = new Stack<Types.ACTIONS>();
    private ArrayList<StateObservation> acted_state = new ArrayList<StateObservation>();
    private ArrayList<Types.ACTIONS> executable_action = new ArrayList<Types.ACTIONS>();

    public Agent(StateObservation so, ElapsedCpuTimer elapsedTimer) {}

    public void clear(){
        success_action.clear();
        acted_state.clear();
        action_list.clear();
        executable_action.clear();
        state_stack.clear();
    }

    public void init(StateObservation stateObs){
        state_stack.push(stateObs);
        action_list.add(null);
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

    public Types.ACTIONS DFS(){
        while(true){
            StateObservation state=state_stack.peek();

            if(isInActedState(state)){
                state_stack.pop();
                action_list.remove(action_list.size()-1);
                continue;
            }
            acted_state.add(state);

            if (state.isGameOver()){
                if (state.getGameWinner()==Types.WINNER.PLAYER_WINS){
                    //回溯
                    StateObservation st = state_stack.pop();
                    while(!state_stack.isEmpty()){
                        StateObservation state_before = state_stack.pop();
                        Types.ACTIONS act=action_list.get(action_list.size()-1);
                        StateObservation stcopy = state_before.copy();
                        stcopy.advance(act);
                        if (st.equalPosition(stcopy)){
                            success_action.add(act);
                            st=state_before.copy();
                            action_list.remove(action_list.size()-1);
                        }
                        else{
                            action_list.remove((action_list.size()-2));
                        }
                    }
                    return success_action.peek();
                }
                else {
                    state_stack.pop();
                    action_list.remove(action_list.size()-1);
                    continue;
                }
            }

            for(Types.ACTIONS action:executable_action){
                StateObservation stCopy = state.copy();
                stCopy.advance(action);
                if (!isInActedState(stCopy) ){
                    state_stack.push(stCopy);
                    action_list.add(action);
                }
            }
        }
    }

    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        Types.ACTIONS action = null;
        init(stateObs);
        action=DFS();
        clear();
        return action;
    }
}
