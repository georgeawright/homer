(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define comparison-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :possible_instances (StructureSet more-concept less-concept)
    :locations (list (Location (list) more-less-space))))
 
(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-[in/de]crease-location-sub"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-[in/de]crease-time-sub"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define increase-sentence-input
  (def-contextual-space :name "s-[in/de]crease.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space time-space conceptual-space)))
(define increase-sentence-output
  (def-contextual-space :name "s-[in/de]crease.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space time-space conceptual-space)))
(define increase-sentence
  (def-frame :name "s-[in/de]crease" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureSet location-sub-frame time-sub-frame)
    :concepts (StructureSet location-concept comparison-concept)
    :input_space increase-sentence-input
    :output_space increase-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) increase-sentence-input))
    :parent_space increase-sentence-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) increase-sentence-input))
    :parent_space increase-sentence-input))
(define late-chunk-location-label
  (def-label :start late-chunk :parent_concept location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) location-sub-frame-input)
		     (Location (list) increase-sentence-input))
    :parent_space location-sub-frame-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) time-sub-frame-input)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space time-sub-frame-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space increase-sentence-input
    :conceptual_space location-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept comparison-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space increase-sentence-input
    :conceptual_space conceptual-space))

(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) increase-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list (list Nan)) more-less-space)
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output))
(define comparison-word-grammar-label
  (def-label :start sentence-word-3 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) increase-sentence-output))))
(define comparison-word-meaning-label
  (def-label :start sentence-word-3 :parent_concept comparison-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (Location (list) increase-sentence-output))))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) increase-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) increase-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-5 :parent_concept pp-directional-time-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))

(define v-super-chunk
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureSet sentence-word-2)
    :right_branch (StructureSet sentence-word-3)))
(define v-super-chunk-label
  (def-label :start v-super-chunk :parent_concept v-concept
    :locations (list v-location
		     (Location (list) increase-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureSet sentence-word-4)
    :right_branch (StructureSet sentence-word-5)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) increase-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureSet v-super-chunk)
    :right_branch (StructureSet pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) increase-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureSet sentence-word-1)
    :right_branch (StructureSet vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) increase-sentence-output))))

(def-relation :start pp-inessive-location-concept :end increase-sentence
  :is_bidirectional True :stable_activation 0.4)
(def-relation :start pp-directional-time-concept :end increase-sentence
  :is_bidirectional True :stable_activation 0.4)
(def-relation :start more-temperature-concept :end increase-sentence
  :is_bidirectional True :stable_activation 0.4)
(def-relation :start less-temperature-concept :end increase-sentence
  :is_bidirectional True :stable_activation 0.4)
