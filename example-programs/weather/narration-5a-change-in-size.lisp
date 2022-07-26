(load "conceptual-spaces/grammar.lisp")
(load "conceptual-spaces/same-different.lisp")
(load "conceptual-spaces/more-less.lisp")
(load "conceptual-spaces/magnitude.lisp")
(load "conceptual-spaces/height.lisp")
(load "conceptual-spaces/goodness.lisp")
(load "conceptual-spaces/size.lisp")
(load "conceptual-spaces/lateness.lisp")
(load "conceptual-spaces/extremeness.lisp")
(load "conceptual-spaces/temperature.lisp")
(load "conceptual-spaces/peripheralness.lisp")
(load "conceptual-spaces/location.lisp")
(load "conceptual-spaces/time.lisp")

(load "frames/ap-jj.lisp")

(load "frames/pp-from-wards-locations.lisp")
(load "frames/pp-between-times.lisp")

(load "frames/s-spread.lisp")

(define input-space
  (def-contextual-space
    :name "input" :parent_concept input-concept :is_main_input True
    :conceptual_spaces (StructureCollection
			temperature-space location-space time-space)))

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 3)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 3)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 5)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 7)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 6)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(define chunk-a
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space))
(define chunk-b
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 0)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 8)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(define chunk-c
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space))
(define chunk-d
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 21)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 12)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(define chunk-e
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space))
(define chunk-f
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 24)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 9)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 11)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 2 8)) location-space))
  :parent_space input-space)

(define chunk-g
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 21)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space))
(define chunk-h
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 6)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 4 8)) location-space))
  :parent_space input-space)

(define chunk-i
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 2)) location-space))
  :parent_space input-space))
(define chunk-j
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 4)) location-space))
  :parent_space input-space))
(define chunk-k
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 6)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 13)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 6 8)) location-space))
  :parent_space input-space)

(define chunk-l
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 24)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 2)) location-space))
  :parent_space input-space))
(define chunk-m
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 23)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 4)) location-space))
  :parent_space input-space))
(define chunk-n
  (def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 6)) location-space))
  :parent_space input-space))
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 14)) temperature-space)
		   (Location (list (list 48)) time-space)
		   (Location (list (list 8 8)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw False
  :locations (list (Location (list) input-space)
		   (Location (list (list 22) (list 22)) temperature-space)
		   (Location (list (list 0) (list 0)) time-space)
		   (Location (list (list 8 2) (list 8 4)) location-space))
  :members (StructureCollection chunk-a chunk-b)
  :quality 1.0
  :activation 1.0
  :parent_space input-space)
(def-chunk
  :is_raw False
  :locations (list (Location (list) input-space)
		   (Location (list (list 21) (list 22) (list 23) (list 23)) temperature-space)
		   (Location (list (list 24) (list 24) (list 24) (list 24)) time-space)
		   (Location (list (list 6 2) (list 6 4) (list 8 2) (list 8 4)) location-space))
  :members (StructureCollection chunk-c chunk-d chunk-e chunk-f)
  :quality 1.0
  :activation 1.0
  :parent_space input-space)
(def-chunk
  :is_raw False
  :locations (list (Location (list) input-space)
		   (Location (list (list 21) (list 22) (list 22) (list 22) (list 23) (list 23) (list 23) (list 24)) temperature-space)
		   (Location (list (list 48) (list 48) (list 48) (list 48) (list 48) (list 48) (list 48) (list 48)) time-space)
		   (Location (list (list 4 2) (list 4 4) (list 6 2) (list 6 4) (list 6 6) (list 8 2) (list 8 4) (list 8 6)) location-space))
  :members (StructureCollection chunk-g chunk-h chunk-i chunk-j chunk-k chunk-l chunk-m chunk-n)
  :quality 1.0
  :activation 1.0
  :parent_space input-space)


