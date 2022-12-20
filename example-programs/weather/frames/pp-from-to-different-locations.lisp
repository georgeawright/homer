(define early-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define late-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-from-to-locations-input
  (def-contextual-space :name "pp[from-to-locations].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space time-space)))
(define pp-from-to-locations-output
  (def-contextual-space :name "pp[from-to-locations].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space location-space time-space)))
(define pp-from-to-locations
  (def-frame :name "pp[from-to-locations]"
    :parent_concept pp-directional-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-from-to-locations-input
    :output_space pp-from-to-locations-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(setattr pp-from-to-locations "early_chunk" early-chunk)
(setattr pp-from-to-locations "late_chunk" late-chunk)
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(define early-chunk-location-label
  (def-label :start early-chunk :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(define late-chunk-location-label
  (def-label :start late-chunk :parent_concept late-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-input))
    :parent_space pp-from-to-locations-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-from-to-locations-input))
    :conceptual_space time-space))
(define location-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept not-same-concept
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) pp-from-to-locations-input))
    :conceptual_space location-space))

(define pp-word-1
  (def-letter-chunk :name "from"
    :locations (list prep-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :abstract_chunk from))
(define pp-word-2
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :abstract_chunk the))
(define pp-word-3
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word-3 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-from-to-locations-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word-3 :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-output))))
(define pp-word-4
  (def-letter-chunk :name "to"
    :locations (list prep-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :abstract_chunk to))
(define pp-word-5
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :abstract_chunk the))
(define pp-word-6
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output))
(define pp-word-6-grammar-label
  (def-label :start pp-word-6 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-from-to-locations-output))))
(define pp-word-6-meaning-label
  (def-label :start pp-word-6 :parent_concept late-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-to-locations-output))))

(define np-super-chunk-1
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :left_branch (StructureSet pp-word-2)
    :right_branch (StructureSet pp-word-3)))
(define pp-super-chunk-1
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :left_branch (StructureSet pp-word-1)
    :right_branch (StructureSet np-super-chunk-1)))

(define np-super-chunk-2
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :left_branch (StructureSet pp-word-5)
    :right_branch (StructureSet pp-word-6)))
(define pp-super-chunk-2
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :left_branch (StructureSet pp-word-4)
    :right_branch (StructureSet np-super-chunk-2)))

(define pp-super-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-from-to-locations-output))
    :parent_space pp-from-to-locations-output
    :left_branch (StructureSet pp-super-chunk-1)
    :right_branch (StructureSet pp-super-chunk-2)))
(define pp-super-super-chunk-label
  (def-label :start pp-super-super-chunk :parent_concept pp-directional-location-concept
    :locations (list pp-location
		     (Location (list) pp-from-to-locations-output))))


(def-relation :start location-concept :end pp-from-to-locations
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start different-location-concept :end pp-from-to-locations
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start more-time-concept :end pp-from-to-locations
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start less-time-concept :end pp-from-to-locations
  :is_bidirectional True :stable_activation 0.5)
