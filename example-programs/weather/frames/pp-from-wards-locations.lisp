(define unidimensional-location-space-parent-concept
  (def-concept :name "" :is_slot True))
(define unidimensional-location-space
  (def-conceptual-space :name "" :parent_concept unidimensional-location-space-parent-concept
    :possible_instances
    (StructureCollection north-south-space west-east-space nw-se-space ne-sw-space)
    :no_of_dimensions 1))
(define location-relation-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(define early-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list (list Nan)) unidimensional-location-space))))
(define late-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list (list Nan)) unidimensional-location-space))))
(def-relation :start early-location-concept :end late-location-concept
  :parent_concept location-relation-concept :conceptual_space unidimensional-location-space
  :activation 1.0)
(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-from-wards-locations-input
  (def-contextual-space :name "pp[from-wards-locations].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection unidimensional-location-space
					    location-space time-space)))
(define pp-from-wards-locations-output
  (def-contextual-space :name "pp[from-wards-locations].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection unidimensional-location-space
					    grammar-space location-space time-space)))
(define pp-from-wards-locations
  (def-frame :name "pp[from-wards-locations]"
    :parent_concept pp-directional-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-relation-concept
				   early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-from-wards-locations-input
    :output_space pp-from-wards-locations-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-from-wards-locations-input))
    :parent_space pp-from-wards-locations-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-from-wards-locations-input))
    :parent_space pp-from-wards-locations-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-from-wards-locations-input))
    :parent_space pp-from-wards-locations-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-from-wards-locations-input))
    :parent_space pp-from-wards-locations-input))
(define early-chunk-location-label
  (def-label :start early-chunk :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-wards-locations-input))
    :parent_space pp-from-wards-locations-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-from-wards-locations-input))
    :conceptual_space time-space))
(define location-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept location-relation-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation
		      (list (list Nan)) (list (list Nan)) unidimensional-location-space)
		     (TwoPointLocation (list) (list) pp-from-wards-locations-input))
    :conceptual_space unidimensional-location-space))

(define pp-word-1
  (def-letter-chunk :name "from"
    :locations (list prep-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :abstract_chunk from))
(define pp-word-2
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :abstract_chunk the))
(define pp-word-3
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word-3 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-from-wards-locations-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word-3 :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-wards-locations-output))))

(define allative-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     pp-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output))
(define allative-chunk-grammar-label
  (def-label :start allative-chunk :parent_concept pp-allative-concept
    :locations (list pp-location
		     (Location (list) pp-from-wards-locations-output))))
(define allative-chunk-meaning-label
  (def-label :start allative-chunk :parent_concept late-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-from-wards-locations-output))))
(define wards-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     pp-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output))
(define wards-chunk-relation
  (def-relation :start allative-chunk :end wards-chunk :parent_concept pp-allative-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) pp-from-wards-locations-output))))
(define pp-word-4
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     pp-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :left_branch (StructureCollection allative-chunk)
    :right_branch (StructureCollection wards-chunk)))
(define pp-word-4-label
  (def-label :start pp-word-4 :parent_concept pp-allative-location-concept
    :locations (list pp-location
		     (Location (list) pp-from-wards-locations-output))))

(define np-super-chunk-1
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :left_branch (StructureCollection pp-word-2)
    :right_branch (StructureCollection pp-word-3)))
(define pp-super-chunk-1
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :left_branch (StructureCollection pp-word-1)
    :right_branch (StructureCollection np-super-chunk-1)))

(define pp-super-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-from-wards-locations-output))
    :parent_space pp-from-wards-locations-output
    :left_branch (StructureCollection pp-super-chunk-1)
    :right_branch (StructureCollection pp-word-4)))
(define pp-super-super-chunk-label
  (def-label :start pp-super-super-chunk :parent_concept pp-directional-location-concept
    :locations (list pp-location
		     (Location (list) pp-from-wards-locations-output))))

(def-relation :start label-concept :end pp-from-wards-locations
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-from-wards-locations
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-from-wards-locations
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-from-wards-locations
  :is_bidirectional True :activation 1.0)