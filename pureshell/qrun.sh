#!bin/bash

# ----------------------------------------------------
# submit SLURM srun jobs
# ----------------------------------------------------

# echos the the usage parameters of qrun
function _qrun_help() {

                    echo "Basic setup parameters for manual tuning"
                    echo "----------------------------------------––––––––––––––-"
                    echo "-t / --time         Defaults to 05:00:00 "
                    echo "-c / --cpu          Defaults to 3 cores"
                    echo "-m / --mem          Defaults to 10G"
                    echo "-d / --detach       Detaches with tmux"
                    echo "                    In order tun leave the session"
                    echo "                    make a second pane using ctrl+b+%"
                    echo "                    and then use 'tmux detach' "
                    echo "---------------------------------------––––––––––––––--"
                    echo "Quick setup for making a large, medium"
                    echo "or small-scale run"
                    echo "--------------------------------------––––––––––––––---"
                    echo "-s / --scale        Can be:"
                    echo "                    -> B (Big)    = 10:00:00 | 10 | 50G"
                    echo "                    -> b          = 00:30:00 | 10 | 50G"
                    # 
                    echo "                    -> M (Meidum) = 10:00:00 | 5  | 5G"
                    echo "                    -> m          = 00:30:00 | 5  | 5G"
                    # 
                    echo "                    -> S (Small)  = 10:00:00 | 1  | 1G"
                    echo "                    -> s          = 00:30:00 | 1  | 1G"
                    # 
                    echo "                    -> T (Tiny)   = 10:00:00 | 1  | 10M"
                    echo "                    -> t          = 00:30:00 | 1  | 10M"
                    echo "----------------------------------––––––––––––––-------"


}

# the new version of qsrun (was removed already) that now works with proper 
# command line arguments, supports quick-setup in different modes and allows
# detachment of the srun session using tmux.
function qrun {

                    # Accepted command line arguments are:

                    # Basic setup parameters for manual tuning
                    # ----------------------------------------––––––––––––––-
                    # -t / --time         Defaults to 05:00:00 
                    # -c / --cpu          Defaults to 3 cores
                    # -m / --mem          Defaults to 10G
                    # -d / --detach       Detaches with tmux
                    # ---------------------------------------––––––––––––––--
                    # Quick setup for making a large, medium
                    # or small-scale run
                    # --------------------------------------––––––––––––––---
                    # -s / --scale        Can be:
                    #                     -> B (Big)    = 10:00:00 | 10 | 50G
                    #                     -> b          = 00:30:00 | 10 | 50G
                    # 
                    #                     -> M (Meidum) = 10:00:00 | 5  | 5G
                    #                     -> m          = 00:30:00 | 5  | 5G
                    # 
                    #                     -> S (Small)  = 10:00:00 | 1  | 1G
                    #                     -> s          = 00:30:00 | 1  | 1G
                    # 
                    #                     -> T (Tiny)   = 10:00:00 | 1  | 10M
                    #                     -> t          = 00:30:00 | 1  | 10M
                    # ----------------------------------––––––––––––––-------

                    # setup default parameters
                    time=05:00:00
                    cpu=3
                    mem=10G
                    detach=0
                    setup=0

                    # parse over command line arguments
                    while [ "$1" != "" ]; do
                        case $1 in

                            -t | --time )           
                                                    shift
                                                    time=$1
                                                    ;;

                            -c | --cpu )    
                                                    shift
                                                    cpu=$1
                                                    ;;
                            
                            -m | --mem )    
                                                    shift
                                                    mem=$1
                                                    ;;

                            -d | --detach )    
                                                    detach=1
                                                    ;;
                            
                            -s | --scale )
                                                    shift
                                                    setup=$1
                                                    ;;

                            -h | --help )           
                                                    _qrun_help
                                                    return
                                                    ;;
                            * )                     
                                                    _qrun_help
                                                    return
                        esac
                        shift
                    done

                    # now make a quick setup from -s / --scale if it was provided
                    if [[ $setup != 0 ]]; then

                        case $setup in 

                        B )                 
                                        time=10:00:00
                                        cpu=10
                                        mem=50
                                        ;;
                        b )
                                        time=00:30:00
                                        cpu=10
                                        mem=50G
                                        ;;

                        M )
                                        time=10:00:00
                                        cpu=5
                                        mem=5G
                                        ;;
                        
                        m )
                                        time=00:30:00
                                        cpu=5
                                        mem=8G
                                        ;;
                        
                        S )
                                        time=10:00:00
                                        cpu=1
                                        mem=1G
                                        ;;
                        
                        s )
                                        time=00:30:00
                                        cpu=1
                                        mem=1G
                                        ;;
                        
                        T )
                                        time=10:00:00
                                        cpu=1
                                        mem=10M
                                        ;;
                        
                        t )
                                        time=00:30:00
                                        cpu=1
                                        mem=10M
                                        ;;
                        * )                     
                                        _qrun_help
                                        return

                        esac

                    fi
                
                    # make either a detached srun session
                    if [[ $detach != 0 ]]; then
                        now=$(date +"%I_%M_%S")
                        session_name="qrun-${now}"
                        tmux new -s $session_name "srun --job-name='$session_name' --time=$time -c $cpu --mem=$mem --pty bash"  
                        tmux attach -t $session_name

                    # or make a default srun session
                    else 
                        srun --time=$time -c $cpu --mem=$mem --pty bash
                    fi 
			}

function quickrun {
					qrun $@
				}