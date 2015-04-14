# Music_Informatic_Final

```
def infinite_playlist(playlist_name, playlist_directory=None):
    all_edges_file = PLAYLIST_DIR + "/" + playlist_name + ".play.pkl"
    all_edges = None
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
