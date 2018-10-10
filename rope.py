from quadtree import Qtree
import math
import csv
import sys
import numpy as np
import random

INF = 999999999

def ReadTracks():

	file = open("datatsne.csv", "r")
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

def GetMapLimits(track):

	xmin = INF
	xmax = -INF
	ymin = INF
	ymax = -INF

	for id in track:
		xmin = min(xmin, track[id]["coord"][0])
		xmax = max(xmax, track[id]["coord"][0])
		ymin = min(ymin, track[id]["coord"][1])
		ymax = max(ymax, track[id]["coord"][1])

	return xmin, xmax, ymin, ymax

def CreateBrownianMotion(n_musics):

	points = np.zeros(n_musics*2).reshape(n_musics,2)

	#Create Brownian Motion
	t = 0
	p = 0
	for i in xrange(n_musics):
		points[i] = np.array([t,p])
		t += 1
		p += random.gauss(0, 1)

	return points

def Rotate(points, start_song, end_song):

	dx1 = float(points[len(points)-1][0] - points[0][0])
	dy1 = float(points[len(points)-1][1] - points[0][1])
	dx2 = float(end_song["coord"][0]) - float(start_song["coord"][0])
	dy2 = float(end_song["coord"][1]) - float(start_song["coord"][1])

	theta1 = math.atan(dy1/dx1)
	theta2 = math.atan(dy2/dx2)

	theta = theta2 - theta1

	R = np.array([math.cos(theta), -math.sin(theta), math.sin(theta), math.cos(theta)]).reshape(2,2)

	for i in range(len(points)):
		points[i] = R.dot(points[i])

	return

def Scale(points, start_song, end_song):

	dx1 = float(points[len(points)-1][0] - points[0][0])
	dy1 = float(points[len(points)-1][1] - points[0][1])
	dx2 = float(end_song["coord"][0]) - float(start_song["coord"][0])
	dy2 = float(end_song["coord"][1]) - float(start_song["coord"][1])

	R = np.array([dx2/dx1, 0, 0, dy2/dy1]).reshape(2,2)

	for i in range(len(points)):
		points[i] = R.dot(points[i])

	return

def Move(points, start_song):

	for i in range(len(points)):
		points[i][0] += float(start_song["coord"][0])
		points[i][1] += float(start_song["coord"][1])

	return

def TransformPoints(points, start_song, end_song):

	Rotate(points, start_song, end_song)
	Scale(points, start_song, end_song)
	Move(points, start_song)

	return

def EuclidDistance(x1, y1, x2, y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def CreatePlaylist(track, points, my_tree):

	playlist_ids = []
	for i in range(points.shape[0]):
		min_dist = INF
		closest_song = -1
		closest_songs = my_tree.RetrieveCellIDs(points[i,0], points[i,1])
		for id in closest_songs:
			if id in playlist_ids:
				continue
			px = points[i,0]
			py = points[i,1]
			tx = track[id]["coord"][0]
			ty = track[id]["coord"][1]
			dist = EuclidDistance(px, py, tx, ty)
			if dist < min_dist:
				min_dist = dist
				closest_song = id
		if closest_song != -1:
			playlist_ids.append(closest_song)

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
	xmin, xmax, ymin, ymax = GetMapLimits(track)

	my_tree = Qtree(xmin,xmax,ymin,ymax)
	my_tree.Divide(1.0)

	for id in track:
		x_coord = track[id]["coord"][0]
		y_coord = track[id]["coord"][1]
		my_tree.Insert(x_coord, y_coord, id)

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

	points = CreateBrownianMotion(n_musics)
	TransformPoints(points, track[start_song], track[end_song])
	playlist = CreatePlaylist(track, points, my_tree)
	PrintPlaylist(playlist)
	
	#print track[start_song]
	#print track[end_song]
	#print points


	return

main()
