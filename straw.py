import math
import csv
import sys
import numpy as np
import random

INF = 999999999

def ReadTracks():

	file = open("data/datatsne.csv", "r")
	reader = csv.reader(file, delimiter=",")

	#Skip the head
	track = {}
	next(reader)
	for row in reader:
		song_id = int(row[0])

		song_info = {}
		song_info["artist_name"] = row[1]
		song_info["track_name"] = row[2]
		song_info["year"] = int(row[3])
		song_info["coord"] = map(float, row[4:])

		track[song_id] = song_info

	file.close()

	return track

def EuclidDistance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def ReadAdjacencyList():

	adj = {}
	file = open("data/adjacencyList.csv", "r")
	reader = csv.reader(file, delimiter=",")
	for row in reader:
		adj[int(row[0])] = map(int, row[1:])

	file.close()

	return adj

def SelectRandomSong(song_ids, track, cur_dist, desire_step, end_song):

	xend = track[end_song]["coord"][0]
	yend = track[end_song]["coord"][1]
	probs = []

	for id in song_ids:
		xt = track[id]["coord"][0]
		yt = track[id]["coord"][1]
		track_dist = EuclidDistance(xt, yt, xend, yend)
		del_v = abs(track_dist-cur_dist)
		probs.append(1.0/(1+abs(del_v - desire_step)))

	probs = np.array(probs)
	probs = probs/np.sum(probs)
	for i in range(1,len(probs)):
		probs[i] = probs[i] + probs[i-1]
	random_number = random.random()
	for i in range(len(probs)):
		if random_number < probs[i]:
			return song_ids[i]

def RandomWalk(playlist_ids, track, adjacencyList, n_musics):

	while len(playlist_ids) < n_musics:
		last_song = playlist_ids[len(playlist_ids)-1]
		next_candidate = []
		for id in adjacencyList[last_song]:
			if id not in playlist_ids:
				next_candidate.append(id)
		playlist_ids.append(random.sample(next_candidate,1)[0])
	return

def RemoveSongs(playlist_ids, track, n_musics):

	while len(playlist_ids) > n_musics:

		max_dist = INF
		best_remove = -1
		for i in range(1,len(playlist_ids)-1):
			before = playlist_ids[i-1]
			after = playlist_ids[i+1]
			xbefore = track[before]["coord"][0]
			ybefore = track[before]["coord"][1]
			xafter = track[after]["coord"][0]
			yafter = track[after]["coord"][1]
			dist = EuclidDistance(xbefore, ybefore, xafter, yafter)
			if dist < max_dist:
				max_dist = dist
				best_remove = i

		playlist_ids = playlist_ids[:best_remove] + playlist_ids[best_remove+1:]

	return playlist_ids

def STRAW(track, start_song, end_song, n_musics, adjacencyList):

	playlist_ids = []
	playlist_ids.append(start_song)

	xstart = track[start_song]["coord"][0]
	ystart = track[start_song]["coord"][1]
	xend = track[end_song]["coord"][0]
	yend = track[end_song]["coord"][1]

	desire_step = EuclidDistance(xstart, ystart, xend, yend)/(n_musics-1)
	cur_song = start_song
	while cur_song != end_song:

		xc = track[cur_song]["coord"][0]
		yc = track[cur_song]["coord"][1]
		cur_dist = EuclidDistance(xc, yc, xend, yend)
		forward = [] #Adjacent songs that are closer to the end song
		backward = [] #Adjacent songs that are farther to the end song
		for id in adjacencyList[cur_song]:
			if id in playlist_ids:
				continue
			xt = track[id]["coord"][0]
			yt = track[id]["coord"][1]
			track_dist = EuclidDistance(xt, yt, xend, yend)
			if track_dist < cur_dist:
				forward.append(id)
			else:
				backward.append(id)

		if len(forward) > 0:
			next_song = SelectRandomSong(forward, track, cur_dist, desire_step, end_song)
		else:
			next_song = SelectRandomSong(backward, track, cur_dist, desire_step, end_song)
		playlist_ids.append(next_song)
		cur_song = next_song

	if len(playlist_ids) < n_musics:
		RandomWalk(playlist_ids, track, adjacencyList, n_musics)
	elif len(playlist_ids) > n_musics:
		playlist_ids = RemoveSongs(playlist_ids, track, n_musics)

	playlist = []
	for id in playlist_ids:
		playlist.append(track[id])

	return playlist

def PrintPlaylist(playlist):

	print "Playlist Created:"
	print "---------------------"
	for song in playlist:
		print song["track_name"] + " by " + song["artist_name"]
	return

def main():

	track = ReadTracks()
	adjacencyList = ReadAdjacencyList()

	start_song = raw_input("Enter ID of the first song: ")
	start_song = int(start_song)
	if start_song not in track:
		sys.stderr.write("Error. Song ID does not exist.\n")
		return

	end_song = raw_input("Enter ID of the last song: ")
	end_song = int(end_song)
	if end_song not in track:
		sys.stderr.write("Error. Song ID does not exist.\n")
		return

	if start_song == end_song:
		sys.stderr.write("Error. First and last songs must be differents.\n")
		return		

	n_musics = raw_input("Enter number of songs in the playlist (must be between 2 and 1000): ")
	n_musics = int(n_musics)
	if n_musics < 2 or n_musics > 1000:
		sys.stderr.write("Error. Input number must be between 2 and 1000.\n")
		return

	playlist = STRAW(track, start_song, end_song, n_musics, adjacencyList)
	PrintPlaylist(playlist)
	return

main()

