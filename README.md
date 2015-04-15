# Music_Informatic_Final

```
class Playback(object):
    threshold = THRESHOLD
    min_branch_probability = 0.18
    max_branch_probability = 0.50
    step_branch_probability = 0.09
    curr_branch_probability = min_branch_probability
    ghost = 1

    def __init__(self, all_edges_, local_audio_, aq_players_, start_beats_, thread=None, curr_md5=None, curr_beat=None):
        from random import choice
        self.all_edges = all_edges_
        self.local_audio = local_audio_
        self.aq_players = aq_players_
        self.start_beats = start_beats_
        self.thread = thread
        if curr_md5 is not None:
            self.curr_md5 = curr_md5
        else:
            self.curr_md5 = choice(self.all_edges.keys())

        self.curr_player = self.aq_players[self.curr_md5]
        self.curr_laf = self.local_audio[self.curr_md5]

        if curr_beat is not None:
            self.curr_beat = curr_beat
        else:
            self.curr_beat = choice(range(len(self.curr_laf.analysis.beats)))
        self.last_branch = [self.curr_beat, self.curr_beat]

    def update(self, *args):
        from random import random, choice
        print "play", self.curr_md5, "beat", self.curr_beat
        cursor_ = args[0]
        branch_cursor_ = args[1]
        last_branch_cursor_ = args[2]
        self.curr_player.play(self.curr_laf.analysis.beats[self.curr_beat])
        self.curr_beat = (self.curr_beat + 1) % len(self.curr_laf.analysis.beats)
        # get candidates
        candidates = self.all_edges[self.curr_md5].get(self.curr_beat, [])
        candidates = [candidates[i] for i in range(len(candidates)) if candidates[i][0] < self.threshold]
        # restrict to local branches if we just changed songs and are resetting the data structures
        if self.thread is not None:
            if self.thread.ejecting():
                candidates = [candidates[i] for i in range(len(candidates)) if candidates[i][1] == self.curr_md5]
        branched = False
        if len(candidates) > 0:
            print len(candidates), "branch candidates, prob =", self.curr_branch_probability
            # print candidates
            # flip a coin
            if random() < self.curr_branch_probability:
                print "Branch!!!"
                branch = choice(candidates)
                changed_song = branch[1] != self.curr_md5
                self.last_branch[0] = [self.curr_beat + self.start_beats[self.curr_md5]]
                self.curr_md5 = branch[1]
                self.curr_beat = branch[2]
                self.curr_player = self.aq_players[self.curr_md5]
                self.curr_laf = self.local_audio[self.curr_md5]
                self.curr_branch_probability = self.min_branch_probability
                self.last_branch[1] = [self.curr_beat + self.start_beats[self.curr_md5]]
                branched = True

                if changed_song:
                    print "********** Changed song **********"
                    # signal that the data loading thread should reset
                    self.last_branch = [self.curr_beat, self.curr_beat]
                    if self.thread is not None:
                        self.thread.eject(self.curr_md5)

            else:
                self.curr_branch_probability = min(self.max_branch_probability,
                                                   self.curr_branch_probability + self.step_branch_probability)
        # update cursor
        t0 = self.curr_beat + self.start_beats[self.curr_md5]
        cursor_.set_xdata(t0)
        cursor_.set_ydata(t0)

        if len(candidates) > 0:
            from numpy import vstack, repeat, array
            t0 = repeat(t0, len(candidates), 0)
            t1 = array([self.start_beats[c[1]] for c in candidates]) + array([c[2] for c in candidates])
            branch_x = vstack((t0, t0, t1, t1, t0)).T.reshape((-1, 1))
            branch_y = vstack((t0, t1, t1, t0, t0)).T.reshape((-1, 1))
            branch_cursor_.set_xdata(branch_x)
            branch_cursor_.set_ydata(branch_y)
            self.ghost = 1
        elif self.ghost >= 4:
            branch_cursor_.set_xdata([])
            branch_cursor_.set_ydata([])
        else:
            self.ghost += 1

        if branched:
            if self.last_branch[0] < self.last_branch[1]:
                last_branch_cursor_.set_color('green')
            else:
                last_branch_cursor_.set_color('red')
            last_branch_x = [self.last_branch[i] for i in [0, 1, 1]]
            last_branch_y = [self.last_branch[i] for i in [0, 0, 1]]
            last_branch_cursor_.set_xdata(last_branch_x)
            last_branch_cursor_.set_ydata(last_branch_y)

        args[0].figure.canvas.draw()


def infinite_playlist(playlist_name, playlist_directory=None):
    
    #Create Pickle File in the playlist directory 
    all_edges_file = PLAYLIST_DIR + "/" + playlist_name + ".play.pkl"   
    
    all_edges = None
    
    #If there is already a file that contains the mapped edges
    if os.path.isfile(all_edges_file):
        print "loading playlist edges"
        with open(all_edges_file, 'rb') as input_:
            all_edges = pickle.load(input_)
        all_songs = [PLAYLIST_DIR + os.sep + md5 + '.mp3' for md5 in all_edges.keys()]
    else:
        all_songs = get_all_songs(playlist_directory)

    print len(all_songs), "songs"

    aq_players = {}
    local_audio = {}
    try:
        local_audio = get_local_audio(all_songs)
        start_beats = get_start_beats(local_audio)
        print start_beats['total'], "total beats"

        if not os.path.isfile(all_edges_file):
            all_edges = get_all_edges(local_audio)
            with open(all_edges_file, 'wb') as output:
                pickle.dump(all_edges, output)

        """
        # for debugging
        import json
        with open('all_edges.json', 'w') as output:
            json.dump(all_edges, output)
        """
        
        #Find all edges between all songs
        total_edges = 0
        for song_i in all_edges.keys():
            song_i_edges = all_edges[song_i]
            for beat_i in song_i_edges.keys():
                song_i_beat_i_edges = song_i_edges[beat_i]
                for _, song_j, beat_j in song_i_beat_i_edges:
                    total_edges += 1
        print total_edges, "total edges"

        s = get_adjacency_matrix(all_edges, start_beats, THRESHOLD)

        for md5, laf in local_audio.iteritems():
            aq_players[md5] = Player(laf)

        from matplotlib.pyplot import figure, plot, show
        fig = figure()
        ax = fig.add_subplot(111)
        ax.spy(s, markersize=1)
        # plot lines around song boundaries
        x = sorted(start_beats.values() * 2)[1:]
        y = sorted(start_beats.values() * 2)[:-1]
        boundaries = [0, 0]
        boundaries[0], = plot(x, y, marker='None', linestyle='-', color='gray')
        boundaries[1], = plot(y, x, marker='None', linestyle='-', color='gray')

        branch_cursor, = plot([], [], color='cyan', marker='s', markersize=5, linestyle='-')
        last_branch_cursor, = plot([], [], color='green', marker='s', markersize=5)
        cursor, = plot([], [], color='magenta', marker='s', markersize=5, linestyle='None')

        # start playing
        dt = 0.001
        # start_md5 = u'0bda1f637253fdeb3cd8e4fb7a3f3683'
        playback = Playback(all_edges, local_audio, aq_players, start_beats)
        timer = fig.canvas.new_timer(interval=dt*1000.0)
        timer.add_callback(playback.update, cursor, branch_cursor, last_branch_cursor)
        timer.start()
        show()

    finally:
        print "cleaning up"
        for player in aq_players.values():
            print "closing aq_player stream"
            player.close_stream()
        for laf in local_audio.values():
            print "unloading local audio"
            laf.unload()
```
