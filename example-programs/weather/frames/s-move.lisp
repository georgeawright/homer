(define move-word
  (def-letter-chunk :name "move" :parent_space grammar-space
    :locations (list vb-location)))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define conceptual-label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))

(define ap-sub-frame-input
  (def-contextual-space :name "ap-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureSet conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space conceptual-space)))
(define ap-sub-frame
  (def-sub-frame :name "s-move-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet conceptual-label-concept)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))

(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-move-location-sub"
    :parent_concept pp-directional-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-move-time-sub"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define move-sentence-input
  (def-contextual-space :name "s-move.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space time-space conceptual-space)))
(define move-sentence-output
  (def-contextual-space :name "s-move.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space time-space conceptual-space)))
(define move-sentence
  (def-frame :name "s-move" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureSet ap-sub-frame location-sub-frame time-sub-frame)
    :concepts (StructureSet)
    :input_space move-sentence-input
    :output_space move-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) move-sentence-input))
    :parent_space move-sentence-input))
(define early-chunk-conceptual-label
  (def-label :start early-chunk :parent_concept conceptual-label-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) ap-sub-frame-input)
		     (Location (list) move-sentence-input))
    :parent_space ap-sub-frame-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) move-sentence-input))
    :parent_space move-sentence-input))

(setattr move-sentence "early_chunk" early-chunk)
(setattr move-sentence "late_chunk" late-chunk)
(setattr ap-sub-frame "early_chunk" early-chunk)
(setattr ap-sub-frame "late_chunk" early-chunk)
(setattr time-sub-frame "early_chunk" early-chunk)
(setattr time-sub-frame "late_chunk" late-chunk)
(setattr location-sub-frame "early_chunk" early-chunk)
(setattr location-sub-frame "late_chunk" late-chunk)

(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) time-sub-frame-input)
		     (TwoPointLocation (list) (list) move-sentence-input))
    :parent_space time-sub-frame-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept not-same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) location-sub-frame-input)
		     (TwoPointLocation (list) (list) move-sentence-input))
    :parent_space location-sub-frame-input
    :conceptual_space location-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) move-sentence-input))
    :parent_space move-sentence-input
    :conceptual_space conceptual-space))
  
(define sentence-word-1
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :abstract_chunk the))
(define sentence-word-2
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) move-sentence-output))
    :parent_space ap-sub-frame-output))
(define ap-chunk-grammar-label
  (def-label :start sentence-word-2 :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output))))
(define sentence-word-3
  (def-letter-chunk :name "temperatures"
    :locations (list nn-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-4
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :abstract_chunk will))
(define sentence-word-5
  (def-letter-chunk :name "move"
    :locations (list vb-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :abstract_chunk move-word))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) move-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-6 :parent_concept pp-directional-location-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-7
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) move-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-7 :parent_concept pp-directional-time-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet sentence-word-2)
    :right_branch (StructureSet sentence-word-3)))
(define np-super-chunk-label
  (def-label :start np-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) move-sentence-output))))
(define np-super-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet sentence-word-1)
    :right_branch (StructureSet np-super-chunk)))
(define np-super-super-chunk-label
  (def-label :start np-super-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) move-sentence-output))))
(define np-super-super-chunk-nsubj-label
  (def-label :start np-super-super-chunk :parent_concept nsubj-concept
    :locations (list np-location
		     (Location (list) move-sentence-output))))
(define v-super-chunk
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet sentence-word-4)
    :right_branch (StructureSet sentence-word-5)))
(define v-super-chunk-label
  (def-label :start v-super-chunk :parent_concept v-concept
    :locations (list v-location
		     (Location (list) move-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet sentence-word-6)
    :right_branch (StructureSet sentence-word-7)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) move-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet v-super-chunk)
    :right_branch (StructureSet pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) move-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) move-sentence-output))
    :parent_space move-sentence-output
    :left_branch (StructureSet np-super-super-chunk)
    :right_branch (StructureSet vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) move-sentence-output))))

(def-relation :start pp-directional-location-concept :end move-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start pp-directional-time-concept :end move-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start ap-concept :end move-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start same-temperature-concept :end move-sentence
  :is_bidirectional True :stable_activation 0.2)
